from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify

from accounts.models import UserSettings
from registration.forms import GroupRegisterForm, UserRegisterForm
from utilities.commonutils import get_current_group


def qualify(request, step):
    template = 'qualify_' + step + '.html'
    page_type = 'qualify'
    step_number = int(step[4:])
    if step_number == 0:
        section = 'start'
    elif step_number>0 and step_number<6:
        section = 'eligibility'
    elif step_number>=6 and step_number<9:
        section = 'terms'
    elif step_number == 9:
        section = 'complete'
         
    return render(request, template, {
        'page_type': page_type,
        'section': section,
    })


def register(request):

    page_type = 'register'

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, label_suffix='')
        group_form = GroupRegisterForm(request.POST, label_suffix='')
        if user_form.is_valid() and group_form.is_valid():
            # save each form
            password = user_form.cleaned_data['password1']
            new_user = user_form.save()
            g = group_form.save()
            # associate the user with the group
            u = new_user
            g.users.add(u)
            # set the group as the user's current_group
            settings = UserSettings(user=u, current_group=g)
            settings.save()
            # generate a slug from the group name
            slug = slugify(g.name)[:20]
            g.slug = slug
            g.save()
            # log the new user in
            user = authenticate(username=new_user.username,
                                password=password)
            login(request, user)

            return HttpResponseRedirect(reverse('welcome'))
    else:
        user_form = UserRegisterForm(label_suffix='')
        group_form = GroupRegisterForm(label_suffix='')
        
    return render(request, 'register.html', {
        'group_form': group_form,
        'page_type': page_type,
        'user_form': user_form,
    })


def welcome(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'welcome.html', {
                  'group': group,    
                  })

