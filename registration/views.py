from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from forms import UserRegisterForm


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
