from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from core.models import Meeting
from core.forms import MeetingForm
from core.utils import save_and_add_owner
		
	
def agenda_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Create agenda'
	if request.method == "POST":
		save_and_add_owner(request, MeetingForm(request.POST))
		new_meeting = Meeting.objects.values().order_by('id').reverse()[:1]
 		new_meeting_dictionary = new_meeting[0]
 		meeting_id = str(new_meeting_dictionary['id'])
 		return HttpResponseRedirect(reverse('agenda-edit', args=(meeting_id,)))
	else:
		meeting_form = MeetingForm()
		return render_to_response('agenda_add.html', {'user': request.user, 'meeting_form': meeting_form, 'page_heading': page_heading}, RequestContext(request))
