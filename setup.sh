#!/usr/bin/env bash

set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="resourcehub"
APP_MODULE="app:app"
PORT=8000
BRANCH="$(git -C "$APP_DIR" rev-parse --abbrev-ref HEAD)"

echo "====================================="
echo "Starting server update/setup process"
echo "Repo directory: $APP_DIR"
echo "Branch: $BRANCH"
echo "====================================="

if [ ! -d "$APP_DIR/.git" ]; then
    echo "Error: setup.sh must be run from inside your existing git repository."
    exit 1
fi

echo "Updating package list..."
sudo apt update

echo "Installing required packages if missing..."
sudo apt install -y python3 python3-venv python3-pip git nginx

echo "Pulling latest code from existing repository..."
git -C "$APP_DIR" pull

cd "$APP_DIR"

echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency install."
fi

if [ -f init_db.py ]; then
    echo "Running database initialization..."
    python init_db.py
else
    echo "No init_db.py found, skipping database initialization."
fi

SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "Writing systemd service file..."

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=$SERVICE_NAME Gunicorn Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:$PORT $APP_MODULE
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

echo "Restarting application service..."
sudo systemctl restart $SERVICE_NAME

echo "Restarting nginx..."
sudo systemctl restart nginx

echo "====================================="
echo "Setup complete."
sudo systemctl --no-pager status $SERVICE_NAME || true
echo "====================================="
