from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import Group
from meetings.models import Meeting
from tasks.models import Task


def dashboard(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	
	tasks = Task.objects.filter(group=request.user).order_by('created')
	
	task_headings = ('Description', 'Assigned to', 'Deadline',)
	
	return render(request, 'dashboard.html', {'user': request.user, 'tasks': tasks, 'task_headings': task_headings})
	
