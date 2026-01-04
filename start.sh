#!/bin/bash
source /opt/render/project/src/.venv/bin/activate
python manage.py migrate
python populate.py
python reset_passwords.py
python manage.py runserver 0.0.0.0:$PORT