from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import UserSettings
from utilities.commonutils import get_current_group


def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    user_setup_form = UserSetupForm(instance=request.user)
    group_setup_form = GroupSetupForm(instance=group)

    menu = {'parent': 'account'}
    return render(request, 'account.html', {
                  'menu': menu, 
                  'user_form': user_setup_form,
                  'group_form': group_setup_form})

