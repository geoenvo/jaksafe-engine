#!/bin/bash

cd $(dirname $0)/jaksafe
../bin/python manage.py runserver 0.0.0.0:80
