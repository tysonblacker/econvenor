from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    error = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
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
    
