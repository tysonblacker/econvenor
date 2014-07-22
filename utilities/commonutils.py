import os
import socket


def save_and_add_owner(request, form_object):
    form = form_object
    if form.is_valid():
        temp_form = form.save(commit=False)
        temp_form.owner = request.user
        temp_form.save()


def set_path(local_path, server_path):
    ENVIRONMENT = os.environ['ECONVENOR_ENVIRONMENT']
    if ENVIRONMENT == 'development':
        PATH = local_path
    if ENVIRONMENT == 'test':
        PATH = server_path
    elif ENVIRONMENT == 'production':
        PATH = server_path
    return PATH


def get_current_group(request):
    if not request.user.is_authenticated():
        return None
    user = request.user
    current_group = user.usersettings.current_group
    allowed_users = current_group.users.all()
    if user in allowed_users:         
        return current_group
    else:
        return None
