UNITED BACKEND
==============

Backend to control and manage robots. 

Contain django-admin panel for creating/managing robots and users.
Using robot view in django admin we can see robot live statistics (pagination implemented).

USER AUTHENTICATION:

Backend use JWT for http and ws authentication. For both 'authentication' header is required.
Token can be obtained on endpoint:

    /users/obtain_token/

ROBOT AUTHENTICATION:

Backend use custom token authentication for robot ws authentication. Time valid token is created
based on robot login data, cached and send back to robot. Using this token robot can login to ws.
Implementation for robot authentication is very basic, can be easily extended by additional security
features. Token can be obtained on endpoint:

    /robots/robot/obtain_token

Rules:
  - user can have multiple robots
  - robots can be shared between users
  - user can access only to robots that's are assigned to him
  - user need to logged to access robot/robots
  - user can fetch robot statistics using channel
  - user can change robot state by calling proper view
    
  - robot need to be logged to have channel access
  - robot used token based access to channel
  - robot log to backend using two channels
    * channel for data 
    * channel for commands
  - robot using data channel send his own data frames 
    and get confirmation (for each data frame)
  - robot using commands channel get user sended 
    commands and change his state
    

UNITED TEST ROBOT
-----------------

Test robot is in file robot.py
Update SETTINGS token and serial (based on one created by admin panel)and run it.

It's very simple **PoC**, robot just:
  - obtain his channel token based on his settings
  - log in into two channels
  - send some random data
  - listen for commands and update his internal state CACHE


TODO 
----

I got limited time so **TODO** list looks like that:
  - more tests for channel and edge cases
  - small refactor for RobotStatusChannel
  - creating staging/production compose files
  - adding app logger
  - add some app exceptions and switch to exception flow in some cases
  - switch to better solution for robot statistics logging in case of high data volume
  - add event model to app and log what user do with robot
  - clear requirements


SETUP
-----

**NOT TESTED ON MAC**

Project setup:

    $ cp example.envs .envs
    $ docker-compose build
    $ docker-compose up --detach
    $ docker-compose exec backend python manage.py collectstatic

Create admin user:

    $ docker-compose exec backend python manage.py createsuperuser

Login and create tests robots in django admin:

    127.0.0.1:8000/admin/robots/robot/add/

Close:
    
    $ docker-compose down


COMMANDS
--------

Run:

    $ docker-compose up

Stop:

    $ docker-compose down

Stop destroy data:

    $ docker-compose down --volume

black:
    
    $ black -S --config black.conf app/

flake8:

    $ flake8 --config flake8 app/

tests:

    $ docker-compose run backend pytest --ds settings.development
