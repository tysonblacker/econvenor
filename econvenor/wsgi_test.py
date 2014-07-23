"""
WSGI config for econvenor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

project_path = '/home/econvenor/webapps/test_econvenor'
virtualenv_path = '/home/econvenor/.virtualenvs/test'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'econvenor.settings')

site.addsitedir(virtualenv_path + '/lib/python2.7/site-packages')
activate_this = os.path.expanduser(virtualenv_path + '/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = project_path + '/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path = [project_path + '/econvenor', project_path + '/any_otherPaths?',
            project_path] + sys.path

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
