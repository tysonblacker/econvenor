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

if socket.gethostname() == 'web439.webfaction.com':
	site.addsitedir(
		'/home/econvenor/.virtualenvs/env/lib/python2.7/site-packages'
	)
	activate_this = os.path.expanduser(
		"~/.virtualenvs/env/bin/activate_this.py"
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
else:
	from django.core.wsgi import get_wsgi_application
	application = get_wsgi_application()
