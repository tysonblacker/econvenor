from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify

from accounts.models import UserSettings
from registration.forms import GroupSetupForm, \
                               UserRegisterForm, \
                               UserSetupForm
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
        form = UserRegisterForm(request.POST, label_suffix='')
        if form.is_valid():
            password = form.cleaned_data['password1']
            new_user = form.save()
            user = authenticate(username=new_user.username,
                                password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('initialise'))
    else:
        form = UserRegisterForm(label_suffix='')

    return render(request, 'register.html', {
        'form': form,
        'page_type': page_type,
    })

   
def initialise(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    page_type = 'register'    

    if request.method == "POST":
        user_setup_form = UserSetupForm(request.POST, instance=request.user,
                                        label_suffix='')
        group_setup_form = GroupSetupForm(request.POST, label_suffix='')
    
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
            return HttpResponseRedirect(reverse('welcome'))
    else:
        user_setup_form = UserSetupForm(label_suffix='')   
        group_setup_form = GroupSetupForm(label_suffix='')   
    
    return render(request, 'initialise.html', {
                  'group_form': group_setup_form,
                  'page_type': page_type,
                  'user_form': user_setup_form,
                  })


def welcome(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'welcome.html', {
                  'group': group,    
                  })

