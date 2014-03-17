#!/bin/bash

# A script to run the eConvenor "reminders" management command
# To be run once each day by cron


cd /home/econvener/DjangoProjects/econvenor
source /home/econvenor/bin/virtualenvwrapper.sh
workon env
python manage.py reminders
deactivate env
