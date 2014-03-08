from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import Account
from accounts.forms import AccountForm, AccountSetupForm
from utilities.commonutils import save_and_add_owner


def account(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    page_heading = 'Account settings'
    
    if request.method == "POST":
        save_and_add_owner(request, AccountForm(request.POST))
        return HttpResponseRedirect(reverse('dashboard'))

	account = Account.objects.all()
	acctform = 'fdjkslfjdkl'
	
    return render(request, 'account.html', {'user': request.user, 'account_form': acctnbform, 'page_heading': page_heading})
	

def account_setup(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    
    page_heading = 'Account setup'
    
    if request.method == "POST":
        pass
    
    form = AccountSetupForm()   
    
    return render(request, 'account_setup.html', {'user': request.user, 'form': form, 'page_heading': page_heading})
