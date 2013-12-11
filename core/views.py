from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.forms import HiddenInput, Textarea
from django.contrib.auth import authenticate, login, logout

from core.models import Decision, Item, Meeting, Participant, Task
from core.forms import DecisionForm, ItemForm, MeetingForm, ParticipantForm, TaskForm, ItemForm


# Helper functions

def save_and_add_owner(request, form_object):
	form = form_object
	if form.is_valid():
		temp_form = form.save(commit=False)
		temp_form.owner = request.user
		temp_form.save()
    

# View functions

def index(request):
	error = ''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('dashboard'))
			else:
				error = 'Your account is not active.'
		else:
			error = 'The credentials you entered are not valid. Try again.'
	return render_to_response('index.html', {'error': error}, RequestContext(request))


def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def dashboard(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	return render_to_response('dashboard.html', RequestContext(request))
	

def participant_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	participants = Participant.objects.filter(owner=request.user).order_by('first_name')
	page_heading = 'Participants'
	table_headings = ('First name', 'Last name', 'Email address', 'Phone number',)
	return render_to_response('participant_list.html', {'participants': participants, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))


def participant_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Add a participant'
	if request.method == "POST":
		save_and_add_owner(request, ParticipantForm(request.POST))
		return HttpResponseRedirect(reverse('participant-list'))
	else:
		participant_form = ParticipantForm()
	return render_to_response('participant_add.html', {'participant_form': participant_form, 'page_heading': page_heading}, RequestContext(request))
			 
		
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
	return render_to_response('participant_edit.html', {'participant_form': participant_form, 'page_heading': page_heading, 'participant_id': participant_id}, RequestContext(request))


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
			new_task_form = TaskForm()
	elif request.method == "POST" and request.POST['new_task_button']=='new_task_save':
		save_and_add_owner(request, TaskForm(request.POST))
		new_task_form = {}
	return render_to_response('participant_view.html', {'participant': participant, 'page_heading': page_heading, 'table_headings': table_headings, 'tasks': tasks, 'new_task_form': new_task_form}, RequestContext(request))


def task_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	tasks = Task.objects.all().order_by('deadline')
	page_heading = 'Tasks'
	table_headings = ('Description', 'Assigned to', 'Deadline', 'Status',)
	return render_to_response('task_list.html', {'tasks': tasks, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	

def task_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Add a task'
	if request.method == "POST":
		save_and_add_owner(request, TaskForm(request.POST))
		return HttpResponseRedirect(reverse('task-list'))
	else:
		task_form = TaskForm()
	return render_to_response('task_add.html', {'task_form': task_form, 'page_heading': page_heading}, RequestContext(request))
	
		
def task_edit(request, task_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	task = Task.objects.get(pk=int(task_id))
	page_heading = task
	if request.method == "POST" and request.POST['button']=='delete-task':
		task.delete()
		return HttpResponseRedirect(reverse('task-list'))
	elif request.method == "POST":
		save_and_add_owner(request, TaskForm(request.POST, instance=task))
		return HttpResponseRedirect(reverse('task-list'))
	else:
		task_form = TaskForm(instance=task)		
	return render_to_response('task_edit.html', {'task_form': task_form, 'page_heading': page_heading, 'task_id': task_id}, RequestContext(request))


def agenda_list(request):
	agendas = Meeting.objects.all()
	page_heading = 'Agendas'
	table_headings = ('Meeting number', 'Date', 'Location',)
	return render_to_response('agenda_list.html', {'agendas': agendas, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	
	
def agenda_add(request):
	page_heading = 'Create agenda'
	if request.method == "POST":
		meeting_form = MeetingForm(request.POST)
		if meeting_form.is_valid():
			meeting_form.save()
			new_meeting = Meeting.objects.values().order_by('id').reverse()[:1]
 			new_meeting_dictionary = new_meeting[0]
 			meeting_id = str(new_meeting_dictionary['id'])
 			return HttpResponseRedirect(reverse('agenda-edit', args=(meeting_id,)))
	else:
		meeting_form = MeetingForm()
		return render_to_response('agenda_add.html', {'meeting_form': meeting_form, 'page_heading': page_heading}, RequestContext(request))


def agenda_edit(request, meeting_id):
	page_heading = 'Create agenda for meeting'
	task_list_headings = ('Description', 'Assigned to', 'Deadline')
	meeting = Meeting.objects.get(pk=int(meeting_id))
	AgendaItemFormSet = inlineformset_factory(Meeting, Item, extra=0, can_delete=False, widgets={'variety': HiddenInput()})
	AgendaItemFormSetWithSpare = inlineformset_factory(Meeting, Item, extra=1, can_delete=False, widgets={'variety': HiddenInput()})
	main_items = meeting.item_set.filter(variety__exact='main')
	preliminary_items = meeting.item_set.filter(variety__exact='preliminary')
	new_data_form = {}
	existing_data_forms = []
	existing_data_formset = {}
	editable_section = 'none'
	incomplete_task_list = Task.objects.filter(status="Incomplete")
	completed_task_list = Task.objects.filter(status="Complete")
	
	# Management of meeting details
# TO DO: Add a delete button when meeting details are being edited
	if request.method == "POST":
		if 'edit_meeting_details_button' in request.POST:
			if request.POST['edit_meeting_details_button']=='edit_meeting_details':
				existing_data_forms = MeetingForm(instance=meeting)
				editable_section = 'is_meeting_details'
		if 'save_meeting_details_button' in request.POST:
			if request.POST['save_meeting_details_button']=='save_meeting_details':
				new_data_form = MeetingForm(request.POST, instance=meeting)
				if new_data_form.is_valid():
					new_data_form.save()
					editable_section = 'none'
		if 'cancel_meeting_details_button' in request.POST:
			if request.POST['cancel_meeting_details_button']=='cancel_meeting_details':
				editable_section = 'none'
		if 'delete_meeting_button' in request.POST:
			if request.POST['delete_meeting_button']=='delete_meeting':
				meeting.delete()
				return HttpResponseRedirect(reverse('agenda-list'))
				
	# Management of main items 
#TO DO: Allow "save and add another main item" for new forms
	if request.method == "POST":
		# when 'edit_main_items_button' has been pressed
		if 'edit_main_items_button' in request.POST:
			if request.POST['edit_main_items_button']=='edit_main_items':
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=main_items)
				editable_section = 'is_main_items'
		# when 'save_main_items_button' has been pressed
		elif 'save_main_items_button' in request.POST:
			if request.POST['save_main_items_button']=='save_main_items':
				existing_data_formset = AgendaItemFormSet(request.POST, instance=meeting)
				if existing_data_formset.is_valid():
					existing_data_formset.save()
					last_item_added = meeting.item_set.last()
					if last_item_added: # check that last_item_added exists before trying to add data to it
						if last_item_added.variety == '':
							last_item_added.variety = 'main'
							last_item_added.save()
			 		editable_section = 'none'
		# when 'add_main_item_button' has been pressed
		elif 'add_main_item_button' in request.POST:
			if request.POST['add_main_item_button']=='add_main_item':
				existing_data_formset = AgendaItemFormSetWithSpare(instance=meeting, queryset=main_items)
				editable_section = 'is_main_items'
		
	return render_to_response('agenda_edit.html', {'meeting_id': meeting_id, 'meeting': meeting, 'page_heading': page_heading, 'task_list_headings': task_list_headings, 'completed_task_list': completed_task_list, 'incomplete_task_list': incomplete_task_list,'editable_section': editable_section, 'main_items': main_items, 'existing_data_forms': existing_data_forms, 'existing_data_formset': existing_data_formset, 'new_data_form': new_data_form}, RequestContext(request))
	

def minutes_list(request):
	minutes = Meeting.objects.all()
	page_heading = 'Minutes'
	table_headings = ('Meeting number', 'Date', 'Location',)
	return render_to_response('minutes_list.html', {'minutes': minutes, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))


def minutes_edit(request, meeting_id):
	page_heading = 'Create minutes for meeting'
	task_list_headings = ('Description', 'Assigned to', 'Deadline')
	meeting = Meeting.objects.get(pk=int(meeting_id))
	AgendaItemFormSet = inlineformset_factory(Meeting, Item, extra=0, can_delete=True, widgets={'variety': HiddenInput(), 'background': Textarea(attrs={'rows': 3}), 'minute_notes': Textarea(attrs={'rows': 4}),})
	DecisionFormSet = inlineformset_factory(Meeting, Decision, extra=0, can_delete=True, widgets={'item': HiddenInput(), 'description': Textarea(attrs={'rows': 2}),})
	TaskFormSet = inlineformset_factory(Meeting, Task, extra=0, can_delete=True, widgets={'item': HiddenInput(), 'status': HiddenInput()})
	main_items = meeting.item_set.filter(variety__exact='main')
	new_data_form = {}
	existing_data_forms = []
	existing_data_formset = {}
	decision_data_formset = {}
	task_data_formset = {}
	editable_section = 'none'
	incomplete_task_list = Task.objects.filter(status="Incomplete")
	completed_task_list = Task.objects.filter(status="Complete")
	
	if request.method == "POST":
	
		# Management of meeting details
# TO DO: Add form fields for start time, end time, attendance and apologies
		if 'edit_meeting_details_minutes_button' in request.POST:
			if request.POST['edit_meeting_details_minutes_button']=='edit_meeting_details':
				existing_data_forms = MeetingForm(instance=meeting)
				editable_section = 'is_meeting_details'
		if 'save_meeting_details_minutes_button' in request.POST:
			if request.POST['save_meeting_details_minutes_button']=='save_meeting_details':
				new_data_form = MeetingForm(request.POST, instance=meeting)
				if new_data_form.is_valid():
					new_data_form.save()
					editable_section = 'none'
		if 'cancel_meeting_details_minutes_button' in request.POST:
			if request.POST['cancel_meeting_details_minutes_button']=='cancel_meeting_details':
				editable_section = 'none'
		# Management of main items 
		if 'edit_main_items_agenda_button' in request.POST:
			if request.POST['edit_main_items_agenda_button']=='edit_main_items':
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=main_items)
				decision_data_formset = DecisionFormSet(instance=meeting)
				task_data_formset = TaskFormSet(instance=meeting)
				editable_section = 'is_main_items'
		if 'save_main_items_agenda_button' in request.POST:
			if request.POST['save_main_items_agenda_button']=='save_main_items':
				existing_data_formset = AgendaItemFormSet(request.POST, instance=meeting)
				if existing_data_formset.is_valid():
					existing_data_formset.save()
				decision_data_formset = DecisionFormSet(request.POST, instance=meeting)
				if decision_data_formset.is_valid():
					decision_data_formset.save()
				task_data_formset = TaskFormSet(request.POST, instance=meeting)
				if task_data_formset.is_valid():
					task_data_formset.save()
					last_task_added = meeting.task_set.last()
					if last_task_added: # check that last_task_added exists before trying to add data to it
						if last_task_added.status == '':
							last_task_added.status = 'Incomplete'
							last_task_added.save()
				editable_section = 'none'
		if 'add_decision_minutes_button' in request.POST:
			if 'add_decision_item_' in request.POST['add_decision_minutes_button']:
				existing_data_formset = AgendaItemFormSet(request.POST, instance=meeting)
				if existing_data_formset.is_valid():
					existing_data_formset.save()
				decision_data_formset = DecisionFormSet(request.POST, instance=meeting)
				if decision_data_formset.is_valid():
					decision_data_formset.save()
					task_data_formset = TaskFormSet(request.POST, instance=meeting)
				if task_data_formset.is_valid():
					task_data_formset.save()
					last_task_added = meeting.task_set.last()
					if last_task_added:
						if last_task_added.status == '':
							last_task_added.status = 'Incomplete'
							last_item_added.save()
				if 'add_decision_item_' in request.POST['add_decision_minutes_button']:
					item_number = str(request.POST['add_decision_minutes_button'])
					item_number = item_number[18:]
					new_decision = Decision(item_id=int(item_number), meeting_id=meeting_id)
					new_decision.save()
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=main_items)
				decision_data_formset = DecisionFormSet(instance=meeting)				
				task_data_formset = TaskFormSet(instance=meeting)				
				editable_section = 'is_main_items'
			
			
		if 'add_task_minutes_button' in request.POST:
			if 'add_task_item_' in request.POST['add_task_minutes_button']:
				existing_data_formset = AgendaItemFormSet(request.POST, instance=meeting)
				if existing_data_formset.is_valid():
					existing_data_formset.save()
				decision_data_formset = DecisionFormSet(request.POST, instance=meeting)
				if decision_data_formset.is_valid():
					decision_data_formset.save()
					task_data_formset = TaskFormSet(request.POST, instance=meeting)
				if task_data_formset.is_valid():
					task_data_formset.save()
					last_task_added = meeting.task_set.last()
					if last_task_added:
						if last_task_added.status == '':
							last_task_added.status = 'Incomplete'
							last_item_added.save()
				if 'add_task_item_' in request.POST['add_task_minutes_button']:
					item_number = str(request.POST['add_task_minutes_button'])
					item_number = item_number[14:]
					new_task = Task(item_id=int(item_number), meeting_id=meeting_id)
					new_task.save()
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=main_items)
				decision_data_formset = DecisionFormSet(instance=meeting)				
				task_data_formset = TaskFormSet(instance=meeting)				
				editable_section = 'is_main_items'	
						
	return render_to_response('minutes_edit.html', {'meeting_id': meeting_id, 'meeting': meeting, 'page_heading': page_heading, 'task_list_headings': task_list_headings, 'completed_task_list': completed_task_list, 'incomplete_task_list': incomplete_task_list,'editable_section': editable_section, 'main_items': main_items, 'existing_data_forms': existing_data_forms, 'existing_data_formset': existing_data_formset, 'new_data_form': new_data_form, 'decision_data_formset': decision_data_formset, 'task_data_formset': task_data_formset}, RequestContext(request))


def decision_list(request):
	decisions = Decision.objects.all()
	page_heading = 'Decisions'
	table_headings = ('Decision', 'Meeting', 'Agenda item',)
	return render_to_response('decision_list.html', {'decisions': decisions, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
