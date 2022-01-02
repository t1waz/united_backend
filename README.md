UNITED BACKEND
==============


SETUP
-----

    $ cp example.envs .envs
    $ docker-compose build
    $ docker-compose up
    $ docker-compose exec backend python manage.py collectstatic


COMMANDS
--------

black:
    
    $ black -S --config black.conf app/

flake:

    $ flake8 --config flake8 app/

TIME LOG
--------

 - project setup: 0,5 h