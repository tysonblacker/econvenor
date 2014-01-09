from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.forms import HiddenInput, Textarea, DateInput
from django.contrib.auth import authenticate, login, logout

from core.models import Account, Bug, Decision, Feature, Item, Meeting, Participant, Task
from core.forms import AccountForm, BugForm, DecisionForm, FeatureForm, ItemForm, MeetingForm, ParticipantForm, TaskForm, ItemForm
from core.utils import save_and_add_owner, calculate_meeting_duration, find_preceding_meeting_date, convert_markdown_to_html


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
	tasks = Task.objects.filter(owner=request.user, status='Incomplete').order_by('deadline')
	task_headings = ('Description', 'Assigned to', 'Deadline',)
	meetings = Meeting.objects.filter(owner=request.user).order_by('date')
	next_meeting = meetings.last()
	last_meeting = meetings.first()
	account = Account.objects.filter(owner=request.user).last()
	return render_to_response('dashboard.html', {'user': request.user, 'last_meeting': last_meeting, 'next_meeting': next_meeting, 'tasks': tasks, 'task_headings': task_headings, 'account': account}, RequestContext(request))
	

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


def task_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	tasks = Task.objects.filter(owner=request.user).order_by('deadline')
	page_heading = 'Tasks'
	table_headings = ('Description', 'Assigned to', 'Deadline', 'Status',)
	return render_to_response('task_list.html', {'user': request.user, 'tasks': tasks, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	

def task_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Add a task'
	if request.method == "POST":
		save_and_add_owner(request, TaskForm(request.user, request.POST))
		return HttpResponseRedirect(reverse('task-list'))
	else:
		task_form = TaskForm(request.user)
	return render_to_response('task_add.html', {'user': request.user, 'task_form': task_form, 'page_heading': page_heading}, RequestContext(request))
	
		
def task_edit(request, task_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	task = Task.objects.get(pk=int(task_id))
	if task.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	page_heading = task
	if request.method == "POST" and request.POST['button']=='delete-task':
		task.delete()
		return HttpResponseRedirect(reverse('task-list'))
	elif request.method == "POST":
		save_and_add_owner(request, TaskForm(request.user, request.POST, instance=task))
		return HttpResponseRedirect(reverse('task-list'))
	else:
		task_form = TaskForm(request.user, instance=task)		
	return render_to_response('task_edit.html', {'user': request.user, 'task_form': task_form, 'page_heading': page_heading, 'task_id': task_id}, RequestContext(request))


def agenda_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	agendas = Meeting.objects.filter(owner=request.user).order_by('date')
	page_heading = 'Agendas'
	table_headings = ('Date', 'Description', 'Location',)
	return render_to_response('agenda_list.html', {'user': request.user, 'agendas': agendas, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	
	
def agenda_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Create agenda'
	if request.method == "POST":
		save_and_add_owner(request, MeetingForm(request.POST))
		new_meeting = Meeting.objects.values().order_by('id').reverse()[:1]
 		new_meeting_dictionary = new_meeting[0]
 		meeting_id = str(new_meeting_dictionary['id'])
 		return HttpResponseRedirect(reverse('agenda-edit', args=(meeting_id,)))
	else:
		meeting_form = MeetingForm()
		return render_to_response('agenda_add.html', {'user': request.user, 'meeting_form': meeting_form, 'page_heading': page_heading}, RequestContext(request))


def agenda_edit(request, meeting_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Create agenda'
	task_list_headings = ('Description', 'Assigned to', 'Deadline')
	meeting = Meeting.objects.get(pk=int(meeting_id))
	if meeting.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	AgendaItemFormSet = inlineformset_factory(Meeting, Item, extra=0, can_delete=True, widgets={'variety': HiddenInput(), 'background': Textarea(attrs={'rows': 3}),})
	AgendaItemFormSetWithSpare = inlineformset_factory(Meeting, Item, extra=1, can_delete=True, widgets={'variety': HiddenInput(), 'background': Textarea(attrs={'rows': 3}),})
	main_items = meeting.item_set.filter(owner=request.user, variety__exact='main')
	preliminary_items = meeting.item_set.filter(owner=request.user, variety__exact='preliminary')
	new_data_form = {}
	existing_data_forms = []
	existing_data_formset = {}
	editable_section = 'none'
	preceding_meeting_date = find_preceding_meeting_date(request.user, meeting_id)
	incomplete_task_list = Task.objects.filter(owner=request.user, status="Incomplete")
	completed_task_list = []
	if preceding_meeting_date != None:
		completed_task_list = Task.objects.filter(owner=request.user, status="Complete", deadline__gte=preceding_meeting_date).exclude(deadline__gte=meeting.date)
	account = Account.objects.filter(owner=request.user).last()

	
	# Management of meeting details
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
	
	# Management of preliminary items 
	if request.method == "POST":
		# when 'edit_preliminary_items_button' has been pressed
		if 'edit_preliminary_items_button' in request.POST:
			if request.POST['edit_preliminary_items_button']=='edit_preliminary_items':
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=preliminary_items)
				editable_section = 'is_preliminary_items'
		# when 'save_preliminary_items_button' has been pressed
		elif 'save_preliminary_items_button' in request.POST:
			if request.POST['save_preliminary_items_button']=='save_preliminary_items':
				existing_data_formset = AgendaItemFormSet(request.POST, instance=meeting)
				if existing_data_formset.is_valid():
					existing_data_formset.save() # This formset.save() deletes any deleted forms
					for form in existing_data_formset:
						if form.cleaned_data['DELETE'] == True:
							pass
						else:					
							save_and_add_owner(request, form)
					last_item_added = meeting.item_set.last()
					if last_item_added: # check that last_item_added exists before trying to add data to it
						if last_item_added.variety == '':
							last_item_added.variety = 'preliminary'
							last_item_added.save()
			 		editable_section = 'none'
		# when 'add_preliminary_item_button' has been pressed
		elif 'add_preliminary_item_button' in request.POST:
			if request.POST['add_preliminary_item_button']=='add_preliminary_item':
				existing_data_formset = AgendaItemFormSetWithSpare(instance=meeting, queryset=preliminary_items)
				editable_section = 'is_preliminary_items'
					
	# Management of main items 
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
					existing_data_formset.save() # This formset.save() deletes any deleted forms
					for form in existing_data_formset:
						if form.cleaned_data['DELETE'] == True:
							pass
						else:					
							save_and_add_owner(request, form)
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
		
	meeting_duration = calculate_meeting_duration(meeting_id)
	return render_to_response('agenda_edit.html', {'user': request.user, 'meeting_id': meeting_id, 'meeting': meeting, 'meeting_duration': meeting_duration, 'page_heading': page_heading, 'task_list_headings': task_list_headings, 'completed_task_list': completed_task_list, 'incomplete_task_list': incomplete_task_list,'editable_section': editable_section, 'main_items': main_items, 'preliminary_items': preliminary_items, 'existing_data_forms': existing_data_forms, 'existing_data_formset': existing_data_formset, 'new_data_form': new_data_form, 'account': account}, RequestContext(request))


def agenda_distribute(request, meeting_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	meeting = Meeting.objects.get(pk=int(meeting_id))
	if meeting.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	main_items = meeting.item_set.filter(owner=request.user, variety__exact='main')
	preliminary_items = meeting.item_set.filter(owner=request.user, variety__exact='preliminary')
	incomplete_task_list = Task.objects.filter(owner=request.user, status="Incomplete")
	completed_task_list = Task.objects.filter(owner=request.user, status="Complete")
	participants = Participant.objects.filter(owner=request.user).order_by('first_name')
	return render_to_response('agenda_distribute.html', {'user': request.user, 'meeting_id': meeting_id, 'meeting': meeting, 'completed_task_list': completed_task_list, 'incomplete_task_list': incomplete_task_list, 'main_items': main_items, 'preliminary_items': preliminary_items, 'participants': participants}, RequestContext(request))
	

def minutes_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	minutes = Meeting.objects.filter(owner=request.user, agenda_locked=True)
	page_heading = 'Minutes'
	table_headings = ('Meeting number', 'Date', 'Location',)
	return render_to_response('minutes_list.html', {'user': request.user, 'minutes': minutes, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))


def minutes_edit(request, meeting_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Create minutes'
	task_list_headings = ('Description', 'Assigned to', 'Deadline')
	meeting = Meeting.objects.get(pk=int(meeting_id))
	if meeting.owner != request.user:
		return HttpResponseRedirect(reverse('index'))
	meeting.agenda_locked = True
	meeting.save()
	AgendaItemFormSet = inlineformset_factory(Meeting, Item, extra=0, can_delete=True, widgets={'variety': HiddenInput(), 'background': Textarea(attrs={'rows': 3}), 'minute_notes': Textarea(attrs={'rows': 4}),})
	DecisionFormSet = inlineformset_factory(Meeting, Decision, extra=0, can_delete=True, widgets={'item': HiddenInput(), 'description': Textarea(attrs={'rows': 2}), 'owner': HiddenInput(),})
	TaskFormSet = inlineformset_factory(Meeting, Task, extra=0, can_delete=True, widgets={'item': HiddenInput(), 'status': HiddenInput(), 'owner': HiddenInput(), 'deadline': DateInput(attrs={'class': 'datepicker'}),})
	main_items = meeting.item_set.filter(owner=request.user, variety__exact='main')
	new_data_form = {}
	existing_data_forms = []
	existing_data_formset = {}
	decision_data_formset = {}
	task_data_formset = {}
	editable_section = 'none'
	incomplete_task_list = Task.objects.filter(owner=request.user, status="Incomplete")
	completed_task_list = Task.objects.filter(owner=request.user, status="Complete")
	account = Account.objects.filter(owner=request.user).last()
	
	def save_minutes_data(request, meeting):
		existing_data_formset = AgendaItemFormSet(request.POST, instance=meeting)
		if existing_data_formset.is_valid():
			for form in existing_data_formset:
				save_and_add_owner(request, form)
		decision_data_formset = DecisionFormSet(request.POST, instance=meeting)
		if decision_data_formset.is_valid():
			for form in decision_data_formset:
				save_and_add_owner(request, form)
		task_data_formset = TaskFormSet(request.POST, instance=meeting)
		if task_data_formset.is_valid():
			for form in task_data_formset:
				save_and_add_owner(request, form)
		
	if request.method == "POST":
	
		# Management of meeting details
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
				save_minutes_data(request, meeting)
				editable_section = 'none'
		if 'add_decision_minutes_button' in request.POST:
			if 'add_decision_item_' in request.POST['add_decision_minutes_button']:
				save_minutes_data(request, meeting)
				item_number = str(request.POST['add_decision_minutes_button'])
				item_number = item_number[18:]
				new_decision = Decision(item_id=int(item_number), meeting_id=meeting_id, owner=request.user)
				new_decision.save()
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=main_items)
				decision_data_formset = DecisionFormSet(instance=meeting)				
				task_data_formset = TaskFormSet(instance=meeting)				
				editable_section = 'is_main_items'
		if 'add_task_minutes_button' in request.POST:
			if 'add_task_item_' in request.POST['add_task_minutes_button']:
				save_minutes_data(request, meeting)
				item_number = str(request.POST['add_task_minutes_button'])
				item_number = item_number[14:]
				new_task = Task(item_id=int(item_number), meeting_id=meeting_id, owner=request.user, status = 'Incomplete')
				new_task.save()
				existing_data_formset = AgendaItemFormSet(instance=meeting, queryset=main_items)
				decision_data_formset = DecisionFormSet(instance=meeting)				
				task_data_formset = TaskFormSet(instance=meeting)				
				editable_section = 'is_main_items'	
						
	return render_to_response('minutes_edit.html', {'user': request.user, 'meeting_id': meeting_id, 'meeting': meeting, 'page_heading': page_heading, 'task_list_headings': task_list_headings, 'completed_task_list': completed_task_list, 'incomplete_task_list': incomplete_task_list,'editable_section': editable_section, 'main_items': main_items, 'existing_data_forms': existing_data_forms, 'existing_data_formset': existing_data_formset, 'new_data_form': new_data_form, 'decision_data_formset': decision_data_formset, 'task_data_formset': task_data_formset, 'account': account}, RequestContext(request))


def decision_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	decisions = Decision.objects.filter(owner=request.user)
	page_heading = 'Decisions'
	table_headings = ('Decision', 'Meeting', 'Agenda item',)
	return render_to_response('decision_list.html', {'user': request.user, 'decisions': decisions, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	
	
def user_guide(request):
    page_content = convert_markdown_to_html("core/text/user_guide.mkd")
    return render_to_response('markdown_template.html', {'page_content': page_content}, RequestContext(request))


def faqs(request):
    page_content = convert_markdown_to_html("core/text/faqs.mkd")
    return render_to_response('markdown_template.html', {'page_content': page_content}, RequestContext(request))
    

def ask_question(request):
    page_content = convert_markdown_to_html("core/text/ask_question.mkd")
    return render_to_response('markdown_template.html', {'page_content': page_content}, RequestContext(request))
    
      
def account_settings(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Account settings'
	if request.method == "POST":
		save_and_add_owner(request, AccountForm(request.POST))
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		account = Account.objects.filter(owner=request.user).last()
		account_form = AccountForm(instance=account)
	return render_to_response('account_settings.html', {'user': request.user, 'account_form': account_form, 'page_heading': page_heading}, RequestContext(request))
	

def bug_report(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Report a bug'
	if request.method == "POST":
		save_and_add_owner(request, BugForm(request.POST))
		return HttpResponseRedirect(reverse('bug-list'))
	else:
		bug_form = BugForm()
	return render_to_response('bug_report.html', {'user': request.user, 'bug_form': bug_form, 'page_heading': page_heading}, RequestContext(request))
	

def bug_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	bugs = Bug.objects.all()
	page_heading = 'Bugs reported'
	table_headings = ('Bug number', 'Description', 'Date reported',)
	return render_to_response('bug_list.html', {'user': request.user, 'bugs': bugs, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	
	
def feature_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Request a feature/change'
	if request.method == "POST":
		save_and_add_owner(request, FeatureForm(request.POST))
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		feature_form = FeatureForm()
	return render_to_response('feature_request.html', {'user': request.user, 'feature_form': feature_form, 'page_heading': page_heading}, RequestContext(request))
	
	
def feature_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	features = Feature.objects.all()
	page_heading = 'Features/changes requested'
	table_headings = ('Request number', 'Description', 'Date requested',)
	return render_to_response('feature_list.html', {'user': request.user, 'features': features, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
