from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import UserSettings
from accounts.forms import GroupDetailsForm, \
                           PasswordChangeForm, \
                           UserDetailsForm
from common.utils import snapshot_group_details, \
                         snapshot_user_details
from utilities.commonutils import get_current_group


def account(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    menu = {'parent': 'account'}
    return render(request, 'account_settings.html', {
                  'menu': menu,
                  'group': group,
                  })


def password_change(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST, label_suffix='')
        if form.is_valid():
            form.save()
            snapshot_user_details(request.user, password='changed')
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

    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=request.user,
                                label_suffix='')
        if form.is_valid():
            form.save()
            snapshot_user_details(request.user, password='unchanged')
            return HttpResponseRedirect(reverse('account'))
    else:
        form = UserDetailsForm(instance=request.user, label_suffix='')

    menu = {'parent': 'account'}
    return render(request, 'user_edit.html', {
                  'menu': menu,
                  'form': form,
                  })


def group_edit(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = GroupDetailsForm(request.POST, instance=group,
                                label_suffix='')
        if form.is_valid():
            form.save()
            snapshot_group_details(group)
            return HttpResponseRedirect(reverse('account'))
    else:
        form = GroupDetailsForm(instance=group, label_suffix='')

    menu = {'parent': 'account'}
    return render(request, 'group_edit.html', {
                  'menu': menu,
                  'form': form,
                  })
