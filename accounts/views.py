from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import UserSettings
from utilities.commonutils import get_current_group


def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    menu = {'parent': 'account'}
    return render(request, 'account_placeholder.html')

