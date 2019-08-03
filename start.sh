#!/bin/bash

gunicorn -b 0.0.0.0:5000 -p pid -w 2 -e APP_CONFIG_FILE="$(pwd)"/config/env/development.py app_deploy:app -D
