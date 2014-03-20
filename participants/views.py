from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from participants.models import Participant
from participants.forms import AddParticipantForm, EditParticipantForm
from tasks.forms import AddTaskForm
from utilities.commonutils import get_current_group


def participant_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    participants = Participant.lists.by_first_name().filter(group=group)
    selection = 'first_name'
        
    page_heading = 'Participants'
    table_headings = ('First name',
                      'Last name',
                      'Email address',
                      'Phone number',)

    if request.method == "POST":
        if request.POST['button']=='last_name':
            participants = Participant.lists.by_last_name().\
                filter(group=group)
            selection = 'last_name'
        elif request.POST['button']=='newest_first':
            participants = Participant.lists.newest_first().\
                filter(group=group)
            selection = 'newest_first'
                    
    return render(request, 'participant_list.html', {
                  'participants': participants,
                  'page_heading': page_heading,
                  'selection': selection,
                  'table_headings': table_headings,
                  })


def participant_add(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    page_heading = 'Add a participant'
    
    if request.method == "POST":
        form = AddParticipantForm(group, request.POST)
        if form.is_valid():
            form.save(group)    
            return HttpResponseRedirect(reverse('participant-list'))
    else:
        form = AddParticipantForm(group)

    return render(request, 'participant_add.html', {
                  'form': form,
                  'page_heading': page_heading
                  })


def participant_edit(request, participant_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    participant = Participant.objects.get(pk=int(participant_id))
    if participant.group != group:
        return HttpResponseRedirect(reverse('index'))
    
    page_heading = 'Edit %s\'s details' % participant
    
    if request.method == "POST":
        if request.POST['button']=='delete_participant':
            participant.delete()
            return HttpResponseRedirect(reverse('participant-list'))
        elif request.POST['button'] == 'save':
            form = EditParticipantForm(group, request.POST,
                                   instance=participant)
            if form.is_valid():
                form.save(group) 
                return HttpResponseRedirect(reverse('participant-list'))
    else:
        form = EditParticipantForm(group, instance=participant)
        		
    return render(request, 'participant_edit.html', {
                  'form': form,
                  'page_heading': page_heading,
                  'participant_id': participant_id
                  })


def participant_view(request, participant_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    participant = Participant.objects.get(pk=int(participant_id))
    if participant.group != group:
        return HttpResponseRedirect(reverse('index'))
    
    tasks = participant.task_set.all()
    page_heading = participant
    table_headings = ('Description', 'Deadline', 'Status')

    return render(request, 'participant_view.html', {
                  'participant': participant,
                  'page_heading': page_heading,
                  'table_headings': table_headings,
                  'tasks': tasks,
                  })
