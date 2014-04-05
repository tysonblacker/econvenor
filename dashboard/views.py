from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from bugs.models import Bug, Feature
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


def dashboard_admin(request):
    if (not request.user.is_authenticated()) or (request.user.id != 1):
        return HttpResponseRedirect(reverse('index'))

    no_of_users = User.objects.all().count() - 1
    no_of_open_bug_reports = Bug.lists.open_bugs().count()
    no_of_open_feature_requests = Feature.lists.open_features().count()

    menu = {'parent': 'dashboard'}        
    return render(request, 'dashboard_admin.html', {
                  'menu': menu,
                  'no_of_users': no_of_users,
                  'no_of_open_bug_reports': no_of_open_bug_reports,
                  })


	
