#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DJANGO_DIR="$REPO_DIR/mysite"
VENV_DIR="$REPO_DIR/venv"
SERVICE_NAME="resourcehub"
APP_MODULE="mysite.wsgi:application"
PORT=8000
REQUIREMENTS_FILE="$DJANGO_DIR/requirements.txt"
RUN_USER="${SUDO_USER:-$USER}"
BRANCH="$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD)"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
NGINX_SITE="/etc/nginx/sites-available/$SERVICE_NAME"

cleanup_on_error() {
    echo "Setup failed. Showing recent service logs for debugging..."
    sudo systemctl --no-pager status "$SERVICE_NAME" || true
    sudo journalctl -u "$SERVICE_NAME" -n 50 --no-pager || true
}

trap cleanup_on_error ERR

echo "====================================="
echo "Starting Django server setup/update"
echo "Repo directory:   $REPO_DIR"
echo "Django directory: $DJANGO_DIR"
echo "Branch:           $BRANCH"
echo "Run user:         $RUN_USER"
echo "====================================="

if [ ! -d "$REPO_DIR/.git" ]; then
    echo "Error: setup.sh must be run from inside the git repository."
    exit 1
fi

if [ ! -f "$DJANGO_DIR/manage.py" ]; then
    echo "Error: Could not find manage.py at $DJANGO_DIR/manage.py"
    exit 1
fi

if [ "$BRANCH" = "HEAD" ]; then
    echo "Error: repository is in a detached HEAD state. Check out a branch before running setup.sh."
    exit 1
fi

echo "Updating package list..."
sudo apt update

echo "Installing required system packages..."
sudo apt install -y python3 python3-venv python3-pip git nginx

echo "Stopping existing application service..."
sudo systemctl stop "$SERVICE_NAME" || true

echo "Stopping stray gunicorn processes..."
sudo pkill -f "$VENV_DIR/bin/gunicorn" || true
sudo pkill -f "gunicorn.*127.0.0.1:$PORT" || true

echo "Updating repository from GitHub..."
git -C "$REPO_DIR" fetch --prune origin
git -C "$REPO_DIR" reset --hard "origin/$BRANCH"
git -C "$REPO_DIR" clean -fd --exclude venv --exclude .env --exclude .env.*

echo "Rebuilding virtual environment..."
rm -rf "$VENV_DIR"
python3 -m venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
python -m pip install --upgrade pip

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing Python dependencies..."
    python -m pip install -r "$REQUIREMENTS_FILE"
else
    echo "Error: No requirements.txt found at $REQUIREMENTS_FILE"
    exit 1
fi

echo "Applying Django migrations..."
cd "$DJANGO_DIR"
python manage.py migrate
python manage.py check

echo "Writing systemd service file..."
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=$SERVICE_NAME Gunicorn Service
After=network.target

[Service]
User=$RUN_USER
Group=www-data
WorkingDirectory=$DJANGO_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind 127.0.0.1:$PORT $APP_MODULE
Restart=always
RestartSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
EOF

echo "Writing nginx site config..."
sudo tee "$NGINX_SITE" > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf "$NGINX_SITE" "/etc/nginx/sites-enabled/$SERVICE_NAME"
sudo rm -f /etc/nginx/sites-enabled/default

echo "Testing nginx config..."
sudo nginx -t

echo "Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

echo "Restarting services..."
sudo systemctl restart "$SERVICE_NAME"
sudo systemctl restart nginx

echo "====================================="
echo "resourcehub service status:"
sudo systemctl --no-pager status "$SERVICE_NAME" || true
echo "====================================="
echo "nginx status:"
sudo systemctl --no-pager status nginx || true
echo "====================================="
echo "Active gunicorn processes:"
ps aux | grep gunicorn | grep -v grep || true
echo "====================================="
echo "Done."
