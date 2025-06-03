#!/bin/bash

brew services start redis
python3.11 manage.py runserver
# brew services stop redis – после остановки проекта, не забывать отключать redis