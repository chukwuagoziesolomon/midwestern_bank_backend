#!/bin/bash
python manage.py migrate
python populate.py
python manage.py runserver 0.0.0.0:$PORT