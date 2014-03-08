from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from forms import UserRegisterForm

from utils import process_account_request


def user_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                error = 'Your account is not active.'
        else:
            error = 'The credentials you entered are not valid. Try again.'

    return render(request, 'user_login.html', {'error': error})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
  

def user_register(request):
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
    return render(request, "user_register.html", {
        'form': form,
    })

