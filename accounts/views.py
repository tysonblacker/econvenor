from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.forms import GroupSetupForm, UserSetupForm
from accounts.models import UserSettings

def account(request):
    pass


def account_setup(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == "POST":
        user_setup_form = UserSetupForm(request.POST, instance=request.user)
        group_setup_form = GroupSetupForm(request.POST)
    
        if user_setup_form.is_valid() and group_setup_form.is_valid():
            # save each form
            user_setup_form.save()
            g = group_setup_form.save()
            # associate the user with the group
            u = request.user
            g.users.add(u)
            # set the group as the user's current_group
            settings = UserSettings(user=u, current_group=g)
            settings.save()
           
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        user_setup_form = UserSetupForm()   
        group_setup_form = GroupSetupForm()   
    
    return render(request, 'account_setup.html', {
        'user_form': user_setup_form,
        'group_form': group_setup_form})
    
   
