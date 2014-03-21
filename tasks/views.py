from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from tasks.models import Task
from tasks.forms import AddTaskForm, EditTaskForm
from utilities.commonutils import get_current_group


def task_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    tasks = Task.lists.all_tasks().filter(group=group)
    selection = 'all'
    
    page_heading = 'Tasks'
    table_headings = ('Description',
                      'Assigned to',
                      'Deadline',
                      'Status',
                      )
    
    if request.method == "POST":
        if request.POST['button']=='complete':
            tasks = Task.lists.complete_tasks().filter(group=group)
            selection = 'complete'
        elif request.POST['button']=='incomplete':
            tasks = Task.lists.incomplete_tasks().filter(group=group)
            selection = 'incomplete'
        elif request.POST['button']=='overdue':
            tasks = Task.lists.overdue_tasks().filter(group=group)
            selection = 'overdue'
 
    return render(request, 'task_list.html', {
	              'request': request,
	              'tasks': tasks,
	              'selection': selection,
	              'page_heading': page_heading,
	              'table_headings': table_headings
	              })


def task_add(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    page_heading = 'Add a task'
    
    if request.method == "POST":
        form = AddTaskForm(group, request.POST)
        if form.is_valid():
            form.save(group)    
            return HttpResponseRedirect(reverse('task-list'))
    else:
        form = AddTaskForm(group)

    return render(request, 'task_add.html', {
	              'request': request,
	              'form': form,
	              'page_heading': page_heading,
	              })


def task_edit(request, task_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    task = Task.objects.get(pk=int(task_id))
    
    if task.group != group:
        return HttpResponseRedirect(reverse('index'))
    
    page_heading = task
    
    if request.method == "POST":
        if request.POST['button']:
            if request.POST['button']=='delete_task':
                task.delete()
                return HttpResponseRedirect(reverse('task-list'))
            else:
                form = EditTaskForm(group, request.POST, instance=task)
                if form.is_valid():
                    form.save(group)    
                    return HttpResponseRedirect(reverse('task-list'))
    else:
        form = EditTaskForm(group, instance=task)
        		
    return render(request, 'task_edit.html', {
	              'request': request,
                  'form': form,
                  'page_heading': page_heading,
                  'task_id': task_id,
                  })
    
    
    
    
    
    
    
