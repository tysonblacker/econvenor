"""
WSGI config for econvenor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site
import socket

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "econvenor.settings")

ENVIRONMENT = os.environ['ECONVENOR_ENVIRONMENT']

if ENVIRONMENT == 'development':
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
elif ENVIRONMENT == 'test':
	site.addsitedir(
		'/home/econvenor/.virtualenvs/test/lib/python2.7/site-packages'
	)
	activate_this = os.path.expanduser(
		"~/.virtualenvs/test/bin/activate_this.py"
	)
	execfile(activate_this, dict(__file__=activate_this))

	# Calculate the path based on the location of the WSGI script
	project = '/home/econvenor/webapps/test_econvenor/'
	workspace = os.path.dirname(project)
	sys.path.append(workspace)

	sys.path = ['/home/econvenor/webapps/test_econvenor/econvenor',
		'/home/econvenor/webapps/test_econvenor/any_otherPaths?',
		'/home/econvenor/webapps/test_econvenor'
	]+ sys.path

	from django.core.handlers.wsgi import WSGIHandler
	application = WSGIHandler()
elif ENVIRONMENT == 'production':
	site.addsitedir(
		'/home/econvenor/.virtualenvs/production/lib/python2.7/site-packages'
	)
	activate_this = os.path.expanduser(
		"~/.virtualenvs/production/bin/activate_this.py"
	)
	execfile(activate_this, dict(__file__=activate_this))

	# Calculate the path based on the location of the WSGI script
	project = '/home/econvenor/webapps/econvenor/'
	workspace = os.path.dirname(project)
	sys.path.append(workspace)

	sys.path = ['/home/econvenor/webapps/econvenor/econvenor',
		'/home/econvenor/webapps/econvenor/any_otherPaths?',
		'/home/econvenor/webapps/econvenor'
	]+ sys.path

	from django.core.handlers.wsgi import WSGIHandler
	application = WSGIHandler()
