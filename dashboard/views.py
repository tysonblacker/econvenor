from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from accounts.models import Group
from bugs.models import Bug, Feature
from decisions.models import Decision
from meetings.models import DistributionRecord, Meeting
from participants.models import Participant
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

    newest_groups = Group.lists.newest_groups()
    total_accounts = Group.lists.all_groups().count()
    total_agendas = DistributionRecord.objects.filter(doc_type='agenda').\
                    count()
    total_completed_tasks = Task.lists.completed_tasks().count()
    total_decisions = Decision.objects.all().count()
    total_draft_tasks = Task.lists.draft_tasks().count()
    total_free_accounts = Group.objects.filter(account_type='Free').count()
    total_incomplete_tasks = Task.lists.incomplete_tasks().count()
    total_meetings = Meeting.objects.all().count()
    total_minutes = DistributionRecord.objects.filter(doc_type='minutes').\
                    count()
    total_open_bug_reports = Bug.lists.open_bugs().count()
    total_open_feature_requests = Feature.lists.open_features().count()
    total_paid_accounts = Group.objects.filter(account_type='Paid').count()
    total_participants = Participant.objects.all().count()
    total_tasks = Task.objects.all().count()
    total_trial_accounts = Group.objects.filter(account_type='Trial').count()
        
    menu = {'parent': 'dashboard'}        
    return render(request, 'dashboard_admin.html', {
                  'menu': menu,
                  'newest_groups': newest_groups,
                  'total_accounts': total_accounts,
                  'total_agendas': total_agendas,
                  'total_completed_tasks': total_completed_tasks,
                  'total_decisions': total_decisions,
                  'total_draft_tasks': total_draft_tasks,
                  'total_free_accounts': total_free_accounts,
                  'total_incomplete_tasks': total_incomplete_tasks,
                  'total_meetings': total_meetings,
                  'total_minutes': total_minutes,
                  'total_open_bug_reports': total_open_bug_reports,
                  'total_open_feature_requests': total_open_feature_requests,
                  'total_paid_accounts': total_paid_accounts,
                  'total_participants': total_participants,
                  'total_tasks': total_tasks,
                  'total_trial_accounts': total_trial_accounts,
                  })
	
