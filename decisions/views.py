from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from decisions.models import Decision
	
	
def decision_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	decisions = Decision.objects.filter(owner=request.user)
	page_heading = 'Decisions'
	table_headings = ('Decision', 'Meeting', 'Agenda item',)
	return render_to_response('decision_list.html', {'user': request.user, 'decisions': decisions, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
