from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from meetings.models import Meeting
from tasks.models import Task
from utilities.commonutils import get_current_group


def dashboard(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    
    last_meeting = Meeting.lists.past_meetings().filter(group=group).last()
    next_meeting = Meeting.lists.future_meetings().filter(group=group).first()
    if last_meeting:
        days_since_last_meeting = (date.today() - last_meeting.date_scheduled)\
                                  .days
    else:
        days_since_last_meeting = None
    top_overdue_tasks = Task.lists.overdue_tasks().filter(group=group)[:6]
    top_pending_tasks = Task.lists.pending_tasks().filter(group=group)[:6]

    task_headings = ('Description',
                     'Deadline',
                     )

    menu = {'parent': 'dashboard'}        
    return render(request, 'dashboard.html', {
                  'menu': menu,
                  'group': group,
                  'last_meeting': last_meeting,
                  'days_since_last_meeting': days_since_last_meeting,
                  'next_meeting': next_meeting,
                  'top_overdue_tasks': top_overdue_tasks,
                  'top_pending_tasks': top_pending_tasks,
                  'task_headings': task_headings,
                  })
	
