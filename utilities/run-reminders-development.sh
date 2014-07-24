#!/bin/bash

# A script to run the eConvenor "reminders" management command
# To be run once each day by cron


cd /home/econvener/Web/econvenor
source /usr/local/bin/virtualenvwrapper.sh
workon development
python manage.py reminders
deactivate
