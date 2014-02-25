from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout


def user_login(request):
	error = ''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				error = 'Your account is not active.'
		else:
			error = 'The credentials you entered are not valid. Try again.'

	return render_to_response('login.html', {'error': error}, RequestContext(request))


def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))
