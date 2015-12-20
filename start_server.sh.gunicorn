#!/bin/bash

cd $(dirname $0)/jaksafe
../bin/gunicorn jaksafe.wsgi --workers 4 --bind=0.0.0.0:80
