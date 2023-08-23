#!/bin/bash

python manage.py makemigrations smartgallery
python manage.py migrate

python manage.py runserver 0.0.0.0:80