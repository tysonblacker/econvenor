from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import Account, Group
from meetings.models import Meeting
from tasks.models import Task


def dashboard(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	
	account = Account.objects.get(user=request.user)
	
	group = Group.objects.filter(account=account)
	

	tasks = Task.objects.filter(group=group)


	meetings = Meeting.objects.filter(group=group).order_by('created')
	
	next_meeting = meetings.last()
	last_meeting = meetings.first()

	task_headings = ('Description', 'Assigned to', 'Deadline',)
	
	return render(request, 'dashboard.html', {'user': request.user, 'tasks': tasks, 'task_headings': task_headings, 'account': account, 'meetings': meetings})
	
