from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.models import Account
from meetings.models import Meeting
from tasks.models import Task


def dashboard(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	tasks = Task.objects.filter(owner=request.user, status='Incomplete').order_by('deadline')
	task_headings = ('Description', 'Assigned to', 'Deadline',)
	meetings = Meeting.objects.filter(owner=request.user).order_by('date')
	next_meeting = meetings.last()
	last_meeting = meetings.first()
	account = Account.objects.filter(owner=request.user).last()
	return render_to_response('dashboard.html', {'user': request.user, 'last_meeting': last_meeting, 'next_meeting': next_meeting, 'tasks': tasks, 'task_headings': task_headings, 'account': account}, RequestContext(request))
	
