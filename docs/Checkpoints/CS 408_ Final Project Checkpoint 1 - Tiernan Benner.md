Final Project Checkpoint 1

## Task 1:

[Github Project Repo](https://github.com/33TIERNAN33/CS408ProjectRepo)  
[Github V1 Tag](https://github.com/33TIERNAN33/CS408ProjectRepo/releases/tag/v1)  
[Project Live Demo URL](http://54.245.50.134)

## Task 2:

Below is the output of my git diff between v0 and v1:  
$ git diff \--shortstat v0 v1  
 7 files changed, 332 insertions(+), 12 deletions(-)

Summary of changes:

* Added [setup.sh](http://setup.sh) script for easy setup, updating, and deployment of the server.  
* Added basic draft for database schema  
* Created basic landing page

Schedule Progress:  
I am looking like I am slightly ahead of the plan laid out in my project specification. I had mostly planned for checkpoint 1 to be getting my project fully approved by Professor Panter and maybe a little bit of a draft done for the database, but I ended up getting those done along with setting up the basic layout of the landing page and getting a script made for easy setup, updating, and deployment of the server.  
The project is currently deployed on an AWS EC2 instance using Nginx and Gunicorn to serve the Django application. The setup.sh script allows the server to be quickly updated from the repository and restarted without manually running multiple setup commands.  
[Project Specification](https://docs.google.com/document/d/1cKJoqwXAiZDKLOppWXlPa-SNdz0E9Nk_D0BbIeDkHX4/edit?usp=sharing)  
Task 3:  
Demo:   
In the video, I demonstrate:

* The deployed application running on EC2  
* The landing page for the CareTrack application  
* The project repository on GitHub  
* The setup.sh deployment script used to update and restart the server  
* The basic database schema draft for the project  
* The Git diff showing changes between version v0 and v1