#!/bin/bash
python3 manage.py migrate
python3 populate.py
python3 reset_passwords.py
python3 manage.py runserver 0.0.0.0:$PORT