from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from tasks.models import Task
from tasks.forms import TaskForm
from utilities.commonutils import save_and_add_owner


def task_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	tasks = Task.objects.filter(owner=request.user).order_by('deadline')
	page_heading = 'Tasks'
	table_headings = ('Description', 'Assigned to', 'Deadline', 'Status',)
	return render_to_response('task_list.html', {'user': request.user, 'tasks': tasks, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	

def task_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Add a task'
	if request.method == "POST":
		save_and_add_owner(request, TaskForm(request.user, request.POST))
		return HttpResponseRedirect(reverse('task-list'))
	else:
		task_form = TaskForm(request.user)
	return render_to_response('task_add.html', {'user': request.user, 'task_form': task_form, 'page_heading': page_heading}, RequestContext(request))
	
		
def task_edit(request, task_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	task = Task.objects.get(pk=int(task_id))
	if task.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	page_heading = task
	if request.method == "POST" and request.POST['button']=='delete-task':
		task.delete()
		return HttpResponseRedirect(reverse('task-list'))
	elif request.method == "POST":
		save_and_add_owner(request, TaskForm(request.user, request.POST, instance=task))
		return HttpResponseRedirect(reverse('task-list'))
	else:
		task_form = TaskForm(request.user, instance=task)		
	return render_to_response('task_edit.html', {'user': request.user, 'task_form': task_form, 'page_heading': page_heading, 'task_id': task_id}, RequestContext(request))


