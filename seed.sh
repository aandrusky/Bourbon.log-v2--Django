#!/bin/bash
rm -rf bourbonLogServerAPI/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations bourbonLogServerAPI
python manage.py migrate bourbonLogServerAPI
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata loggers
python manage.py loaddata logs
python manage.py loaddata flavors
python manage.py loaddata flavorsums