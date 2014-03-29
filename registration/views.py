from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify

from accounts.forms import GroupSetupForm, UserSetupForm
from accounts.models import UserSettings
from registration.forms import UserRegisterForm


def qualify(request, step):
    template = 'qualify_' + step + '.html'
    return render(request, template,)


def register(request, step):
    form = UserRegisterForm(request.POST)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            new_user = form.save()
            user = authenticate(username=new_user.username,
                                password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('account-setup'))
        else:
            form = UserRegisterForm()
    return render(request, 'register_step1.html', {
        'form': form,
    })

   
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
            # generate a slug from the group name
            slug = slugify(g.name)[:20]
            g.slug = slug
            g.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        user_setup_form = UserSetupForm()   
        group_setup_form = GroupSetupForm()   
    
    return render(request, 'register_step2.html', {
                  'user_form': user_setup_form,
                  'group_form': group_setup_form,
                  })

