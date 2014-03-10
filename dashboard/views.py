from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from accounts.models import Group
from meetings.models import Meeting
from tasks.models import Task
from utilities.commonutils import get_current_group


def dashboard(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    user = request.user

    tasks = Task.objects.filter(group=group).order_by('deadline')
    task_headings = ('Description', 'Assigned to', 'Deadline',)
    
    return render(request, 'dashboard.html', {
                  'user': user,
                  'group': group,
                  'tasks': tasks,
                  'task_headings': task_headings,
                  })
	
