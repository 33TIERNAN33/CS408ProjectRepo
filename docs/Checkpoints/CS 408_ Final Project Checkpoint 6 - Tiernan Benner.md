Final Project Checkpoint 6

## Task 1:

[Github Project Repo](https://github.com/33TIERNAN33/CS408ProjectRepo)  
[Github V6 Tag](https://github.com/33TIERNAN33/CS408ProjectRepo/releases/tag/v6)  
[Project Live Demo URL](http://54.245.50.134)

## Task 2:

Below is the output of my git diff between v5 and v6:  
$ git diff \--shortstat v5 v6  
 15 files changed, 1002 insertions(+), 67 deletions(-)

Summary of changes:

* Updated Django settings so deployment values can come from environment variables instead of being hard-coded for local development only.  
* Added `STATIC_ROOT` so production static files can be collected into a single deployment directory.  
* Updated the EC2 setup script to install `curl`, run migrations, run `collectstatic`, and preserve uploaded media.  
* Added automatic creation of a production `.env` file for the Django secret key, debug setting, allowed hosts, and CSRF trusted origins.  
* Updated the systemd service definition so Gunicorn loads the Django production environment file.  
* Updated the Nginx configuration so `/static/` serves collected static assets and `/media/` serves uploaded item images.  
* Added deployment health checks that verify both the direct Gunicorn endpoint and the Nginx proxied endpoint after service restart.  
* Added Checkpoint 6 tests covering the setup script deployment steps and static file configuration.
* Fixed inventory image display sizing so uploaded item photos stay constrained inside the inventory table instead of stretching the page layout.  
* Added server-side exception logging so unexpected application errors are written to a rotating log file for easier debugging on the deployed server.  
* Fixed admin page rendering and readability issues so the Django admin remains usable for managing donors, items, survivors, item requests, and user profiles.  

Schedule Progress:  
I am currently on track with the schedule laid out in my project specification and have completed the main goals planned for Checkpoint 6. This checkpoint focused on the AWS EC2 deployment path, installation script verification, and Nginx configuration. The setup script now handles the production deployment workflow more completely by preparing the virtual environment, applying migrations, collecting static files, creating or reusing the deployment environment file, configuring systemd, configuring Nginx, and checking that the running application responds through both Gunicorn and Nginx.  
The application is also better prepared for the deployed environment because Django can now read the secret key, debug flag, allowed hosts, and CSRF trusted origins from environment variables. Uploaded media remains preserved during server updates, while collected static assets are served directly by Nginx. I also handled several bug fixes during this checkpoint, including inventory image resizing, server-side error logging, and admin page rendering/readability issues. Local tests were expanded to verify the deployment script expectations for this checkpoint.  
[Project Specification](https://docs.google.com/document/d/1cKJoqwXAiZDKLOppWXlPa-SNdz0E9Nk_D0BbIeDkHX4/edit?usp=sharing)

Task 3:  
Demo:   
In the video, I demonstrate:

* The project repository with the Checkpoint 6 deployment changes.  
* The Git tag for v6 once it is created.  
* The Git diff summary between v5 and v6.  
* The setup script sections that install dependencies, rebuild the virtual environment, apply migrations, and run `collectstatic`.  
* The generated Django `.env` configuration used by systemd/Gunicorn.  
* The Nginx configuration for proxying the Django app and serving `/static/` and `/media/`.  
* The setup script health checks for Gunicorn and Nginx.  
* The inventory image sizing fix that keeps uploaded images from disrupting the table layout.  
* The server-side error log file used for debugging unexpected application errors.  
* The admin page fixes that keep admin model pages readable and functional.  
* The local Django test suite running successfully with the Checkpoint 6 tests included.
