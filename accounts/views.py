from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import UserSettings
from accounts.forms import PasswordChangeForm
from utilities.commonutils import get_current_group


def account(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    user = request.user

    menu = {'parent': 'account'}
    return render(request, 'account_settings.html', {
                  'menu': menu,
                  'group': group,
                  'user': user,
                  })
    

def password_change(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST, label_suffix='')
        if form.is_valid():
            form.save()    
            return HttpResponseRedirect(reverse('password-changed'))
    else:
        form = PasswordChangeForm(request.user, label_suffix='')
        
    menu = {'parent': 'account'}
    return render(request, 'password_change.html', {
                  'menu': menu,
                  'form': form,
                  })


def password_changed(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    menu = {'parent': 'account'}
    return render(request, 'password_changed.html', {
                  'menu': menu,
                  })


def user_edit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    pass

        
def group_edit(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    pass
