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

    tasks = Task.lists.incomplete_tasks().filter(group=group)
    selection = 'incomplete'
    table_headings = ('Description', 'Assigned to', 'Deadline',)

    if request.method == "POST":
        if request.POST['button']=='completed':
            tasks = Task.lists.completed_tasks().filter(group=group)
            selection = 'completed'
            table_headings = ('Description', 'Assigned to', 'Completed on',)
        elif request.POST['button']=='incomplete':
            tasks = Task.lists.incomplete_tasks().filter(group=group)
            selection = 'incomplete'
        elif request.POST['button']=='overdue':
            tasks = Task.lists.overdue_tasks().filter(group=group)
            selection = 'overdue'

    menu = {'parent': 'tasks',
            'child': 'manage_tasks',
            'tips': 'manage_tasks'
            }
    return render(request, 'task_list.html', {
                  'menu': menu,
                  'tasks': tasks,
                  'selection': selection,
                  'table_headings': table_headings
                  })


def task_add(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = AddTaskForm(group, request.POST, label_suffix='')
        if form.is_valid():
            form.save(group)
            return HttpResponseRedirect(reverse('task-list'))
    else:
        form = AddTaskForm(group, label_suffix='')

    menu = {'parent': 'tasks', 'child': 'new_task'}
    return render(request, 'task_add.html', {
                  'menu': menu,
                  'form': form,
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
                form = EditTaskForm(group, request.POST, instance=task,
                                    label_suffix='')
#                import pdb; pdb.set_trace()
                if form.is_valid():
                    form.save(group)
                    return HttpResponseRedirect(reverse('task-list'))
    else:
        form = EditTaskForm(group, instance=task, label_suffix='')

    menu = {'parent': 'tasks',
            'child': 'manage_tasks',
            'tips': 'edit_task'
            }
    return render(request, 'task_edit.html', {
                  'menu': menu,
                  'form': form,
                  'page_heading': page_heading,
                  'task_id': task_id,
                  })


