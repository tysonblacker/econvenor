from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from participants.models import Participant
from participants.forms import AddParticipantForm, EditParticipantForm
from tasks.forms import AddTaskForm
from tasks.models import Task
from utilities.commonutils import get_current_group


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
                  
