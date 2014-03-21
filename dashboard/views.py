from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

# from accounts.models import Group
from tasks.models import Task
from utilities.commonutils import get_current_group


def dashboard(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    
    all_overdue_tasks = Task.lists.overdue_tasks().filter(group=group)
    top_overdue_tasks = all_overdue_tasks[:6]
    all_incomplete_tasks = Task.lists.incomplete_tasks().filter(group=group)
    top_incomplete_tasks = all_incomplete_tasks[:6]    
    
    task_headings = ('Description',
                     'Deadline',
                     )

    menu = {'parent': 'dashboard'}        
    return render(request, 'dashboard.html', {
                  'menu': menu,
                  'group': group,
                  'top_overdue_tasks': top_overdue_tasks,
                  'top_incomplete_tasks': top_incomplete_tasks,
                  'task_headings': task_headings,
                  })
	
