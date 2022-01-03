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

tests:

    $ docker-compose run backend pytest --ds settings.development
