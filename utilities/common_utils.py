import socket

from core.models import Account


def save_and_add_owner(request, form_object):
	form = form_object
	if form.is_valid():
		temp_form = form.save(commit=False)
		temp_form.owner = request.user
		temp_form.save()
	

def set_path(local_path, server_path):
	if socket.gethostname() == 'web439.webfaction.com':
		FONT_PATH = server_path
	else:
		FONT_PATH = local_path
	return FONT_PATH
	

def get_group_name(request):
	account = Account.objects.filter(owner=request.user).last()
	group_name = account.group_name
	return group_name
	
	
	

