from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from decisions.models import Decision
from utilities.commonutils import get_current_group	

	
def decision_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
	decisions = Decision.objects.filter(group=group)

	page_heading = 'Decisions'
	table_headings = ('Decision',
	                  'Meeting',
	                  'Agenda item',
	                  )

	return render(request, 'decision_list.html', {
	              'decisions': decisions,
	              'page_heading': page_heading,
	              'table_headings': table_headings,
	              })
