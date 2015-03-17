from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify

from accounts.models import UserSettings
from common.utils import snapshot_group_details, \
                         snapshot_user_details
from participants.models import Participant
from registration.forms import GroupRegisterForm, UserRegisterForm
from registration.utils import send_welcome_email
from utilities.commonutils import get_current_group


def qualify(request, step):
    template = 'qualify_' + step.rstrip('a') + '.html'
    page_type = 'qualify'
    step_number = int(step.lstrip('step').rstrip('a'))
    # Set the page heading
    if step_number == 0:
        section = 'start'
    elif step_number>0 and step_number<6:
        section = 'eligibility'
    elif step_number>=6 and step_number<9:
        section = 'terms'
    elif step_number == 9:
        section = 'complete'
    # Set whether this will be a trial account
    if step[-1:] == 'a':
        trial_account = True
    else:
        trial_account = False

    return render(request, template, {
        'trial_account': trial_account,
        'page_type': page_type,
        'section': section,
    })


def register(request, trial):

    page_type = 'register'
    if trial == 'trial':
        trial_account = True
    else:
        trial_account = False

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, label_suffix='')
        group_form = GroupRegisterForm(request.POST, label_suffix='')
        if user_form.is_valid() and group_form.is_valid():
            # save each form
            password = user_form.cleaned_data['password1']
            new_user = user_form.save()
            group = group_form.save()
            # associate the user with the group
            u = new_user
            group.users.add(u)
            # set the group as the user's current_group
            settings = UserSettings(user=u, current_group=group)
            settings.save()
            # generate a slug from the group name
            slug = slugify(group.name)[:20]
            group.slug = slug
            group.save()
            # set the account status to trial if required
            if trial_account == True:
                group.account_type = 'Trial'
                group.save()
            # save initial snapshots of new user and group details
            snapshot_user_details(u, password='set')
            snapshot_group_details(group)
            # log the new user in
            user = authenticate(username=new_user.username,
                                password=password)
            login(request, user)
            # set the new user up as a participant
            participant = Participant(group=group, email=user.email,
                                      first_name=user.first_name,
                                      last_name=user.last_name)
            participant.save()
            # send the new user a welcome email
            send_welcome_email(group=group, user=user)

            return HttpResponseRedirect(reverse('welcome'))
    else:
        user_form = UserRegisterForm(label_suffix='')
        group_form = GroupRegisterForm(label_suffix='')

    return render(request, 'register.html', {
        'group_form': group_form,
        'page_type': page_type,
        'trial_account': trial_account,
        'user_form': user_form,
    })


def welcome(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'welcome.html', {
                  'group': group,
                  })

