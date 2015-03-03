"""
Participant views from both user and participant perspectives.

All of participant_(list|add|edit|view) are from the user perspective.
"""
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory

from participants.models import Participant
from participants.forms import (
    AddParticipantForm,
    EditParticipantForm,
    MyTasksForm,
)
from participants.auth import authenticate, participant_required
from tasks.forms import AddTaskForm
from tasks.models import Task
from utilities.commonutils import get_current_group


SESSION_KEY = getattr(settings, 'PARTICIPANT_AUTH_SESSION_KEY', 'participant')


def participant_list(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    participants = Participant.lists.active().filter(group=group)
    selection = 'active'
    table_headings = ('Given name',
                      'Family name',
                      'Receiving reminders?',
                      )

    if request.method == "POST":
        if request.POST['button']=='inactive':
            participants = Participant.lists.inactive().filter(group=group)
            selection = 'inactive'
        elif request.POST['button']=='former':
            participants = Participant.lists.former().filter(group=group)
            selection = 'former'

    menu = {'parent': 'participants',
            'child': 'manage_participants',
            'tips': 'manage_participants'
            }
    return render(request, 'participant_list.html', {
                  'menu': menu,
                  'participants': participants,
                  'selection': selection,
                  'table_headings': table_headings,
                  })


def participant_add(request):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = AddParticipantForm(group, request.POST, label_suffix='')
        if form.is_valid():
            form.save(group)
            return HttpResponseRedirect(reverse('participant-list'))
    else:
        form = AddParticipantForm(group, label_suffix='')

    menu = {'parent': 'participants',
            'child': 'new_participant',
            'tips': 'new_participant'
            }
    return render(request, 'participant_add.html', {
                  'menu': menu,
                  'form': form,
                  })


def participant_edit(request, participant_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    participant = Participant.objects.get(pk=int(participant_id))
    if participant.group != group:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        if request.POST['button']=='delete_participant':
            participant.delete()
            return HttpResponseRedirect(reverse('participant-list'))
        elif request.POST['button'] == 'save_participant':
            form = EditParticipantForm(group, request.POST,
                                   instance=participant, label_suffix='')
            if form.is_valid():
                form.save(group)
                return HttpResponseRedirect(reverse('participant-list'))
    else:
        form = EditParticipantForm(group, instance=participant,
                                   label_suffix='')

    menu = {'parent': 'participants',
            'child': 'manage_participants',
            'tips': 'edit_participant'
            }
    return render(request, 'participant_edit.html', {
                  'menu': menu,
                  'form': form,
                  'participant_id': participant_id
                  })


def participant_view(request, participant_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    participant = Participant.objects.get(pk=int(participant_id))
    if participant.group != group:
        return HttpResponseRedirect(reverse('index'))

    incomplete_tasks = Task.lists.incomplete_tasks().\
                       filter(participant=participant)
    table_headings = ('Description', 'Deadline',)

    menu = {'parent': 'participants', 'child': 'manage_participants'}
    return render(request, 'participant_view.html', {
                  'menu': menu,
                  'participant': participant,
                  'table_headings': table_headings,
                  'incomplete_tasks': incomplete_tasks,
                  })


def my_tasks_auth(request, participant_id, token):
    """Authenticate a participant using a token from the last 30 days."""
    authenticate(request, participant_id, token)
    return HttpResponseRedirect(reverse('my-tasks'))


@participant_required
def my_tasks(request):
    """
    Displays a list of the participant's outstanding tasks and
    allows the participant to mark them as completed.
    """
    participant_id = request.session.get(SESSION_KEY).get('id')
    participant = Participant.objects.get(pk=int(participant_id))

    MyTasksFormSet = modelformset_factory(
        Task,
        form=MyTasksForm,
        extra=0,
    )
    formset_queryset=Task.lists.incomplete_tasks().\
                filter(participant=participant)

    if request.method == "POST":
        formset = MyTasksFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                participant_owns_task = (
                    form.cleaned_data['id'].participant == participant
                )
                completion_date_set = form.cleaned_data['completion_date']
                if participant_owns_task and completion_date_set:
                    form.save()
            return HttpResponseRedirect(reverse('my-tasks-done'))
    else:
        formset = MyTasksFormSet(queryset=formset_queryset)

    return render(request, 'my_tasks.html', {
                  'participant': participant,
                  'formset_has_contents': formset_queryset.exists(),
                  'formset': formset,
                  })


@participant_required
def my_tasks_done(request):
    """
    Shows a success page with a list of the tasks which have been
    marked as completed, and a list of tasks still outstanding.
    """
    today = date.today()

    participant_id = request.session.get(SESSION_KEY).get('id')
    participant = Participant.objects.get(pk=int(participant_id))

    tasks_outstanding = Task.lists.incomplete_tasks().\
        filter(participant=participant)
    tasks_just_completed = Task.lists.completed_tasks().\
        filter(participant=participant).\
        filter(modified__gte=today).\
        filter(participant_set_status_completed=True)

    return render(request, 'my_tasks_done.html', {
                  'participant': participant,
                  'no_of_tasks_outstanding': tasks_outstanding.count(),
                  'tasks_just_completed': tasks_just_completed,
                  })
