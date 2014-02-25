from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from core.models import Account
from core.forms import AccountForm
    
      
def account_settings(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Account settings'
	if request.method == "POST":
		save_and_add_owner(request, AccountForm(request.POST))
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		account = Account.objects.filter(owner=request.user).last()
		account_form = AccountForm(instance=account)
	return render_to_response('account_settings.html', {'user': request.user, 'account_form': account_form, 'page_heading': page_heading}, RequestContext(request))
	

