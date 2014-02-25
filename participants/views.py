from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from core.models import Participant
from core.forms import ParticipantForm, TaskForm
from core.utils import save_and_add_owner


def participant_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	participants = Participant.objects.filter(owner=request.user).order_by('first_name')
	page_heading = 'Participants'
	table_headings = ('First name', 'Last name', 'Email address', 'Phone number',)
	return render_to_response('participant_list.html', {'user': request.user, 'participants': participants, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))


def participant_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Add a participant'
	if request.method == "POST":
		save_and_add_owner(request, ParticipantForm(request.POST))
		return HttpResponseRedirect(reverse('participant-list'))
	else:
		participant_form = ParticipantForm()
	return render_to_response('participant_add.html', {'user': request.user, 'participant_form': participant_form, 'page_heading': page_heading}, RequestContext(request))
			 
		
def participant_edit(request, participant_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	participant = Participant.objects.get(pk=int(participant_id))
	if participant.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Edit %s/s details' % participant
	if request.method == "POST" and request.POST['button']=='delete-participant':
		participant.delete()
		return HttpResponseRedirect(reverse('participant-list'))
	elif request.method == "POST":
		save_and_add_owner(request, ParticipantForm(request.POST, instance=participant))
		return HttpResponseRedirect(reverse('participant-list'))
	else:
		participant_form = ParticipantForm(instance=participant)		
	return render_to_response('participant_edit.html', {'user': request.user, 'participant_form': participant_form, 'page_heading': page_heading, 'participant_id': participant_id}, RequestContext(request))


def participant_view(request, participant_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	participant = Participant.objects.get(pk=int(participant_id))
	if participant.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	tasks = participant.task_set.all()
	page_heading = participant
	table_headings = ('Description', 'Deadline', 'Status')
	new_task_form = {}
	if 'add_task_button' in request.POST:
		if request.method == "POST" and request.POST['add_task_button']=='add_task':
			new_task_form = TaskForm(request.user)
	elif request.method == "POST" and request.POST['new_task_button']=='new_task_save':
		save_and_add_owner(request, TaskForm(request.user, request.POST))
		new_task_form = {}
	return render_to_response('participant_view.html', {'user': request.user, 'participant': participant, 'page_heading': page_heading, 'table_headings': table_headings, 'tasks': tasks, 'new_task_form': new_task_form}, RequestContext(request))
