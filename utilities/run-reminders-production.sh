#!/bin/bash

# A script to run the eConvenor "reminders" management command
# To be run once each day by cron


cd ~/webapps/econvenor/econvenor
source ~/.bashrc
source ~/bin/virtualenvwrapper.sh
workon env
python2.7 manage.py reminders
deactivate env
