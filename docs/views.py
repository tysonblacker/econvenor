import json

from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.forms import DateInput, HiddenInput, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from accounts.models import Group
from decisions.models import Decision
from docs.forms import AgendaForm, MinutesForm
from docs.models import Item
from docs.pdfs import create_pdf_agenda, \
                      get_pdf_contents
from docs.utils import add_item, \
                       calculate_meeting_duration, \
                       calculate_meeting_end_time, \
                       delete_item, \
                       distribute_agenda, \
                       get_completed_tasks_list, \
                       get_formatted_meeting_duration, \
                       move_item, \
                       save_formlist
from meetings.models import Meeting
from participants.models import Participant
from tasks.models import Task
from utilities.commonutils import get_current_group


def agenda_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    agendas = Meeting.objects.filter(group=group)
    page_heading = 'Agendas'
    table_headings = ('Date', 'Meeting Number', 'Meeting Type',)

    return render(request, 'agenda_list.html', {
                  'agendas': agendas,
                  'page_heading': page_heading,
                  'table_headings': table_headings
                  })
    

def agenda_edit(request, meeting_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    request_type = 'refresh'
    page_heading = 'Create agenda'
    task_list_headings = ('Description',
                          'Assigned to',
                          'Deadline')

    items = meeting.item_set.filter(group=group).order_by('item_no')
    AgendaForm.base_fields['explainer'].queryset =\
        Participant.objects.filter(group=group)
    

    incomplete_tasks_list = Task.lists.incomplete_tasks().filter(group=group)
    completed_tasks_list = get_completed_tasks_list(group)

    if request.method == "POST" and 'ajax_button' in request.POST:
        request_type = 'ajax'
        if request.POST['ajax_button'] != 'page_refresh':              
            save_formlist(request, group, meeting, items, 'agenda')
        if request.POST['ajax_button'][0:10]=='add_button':
            add_item(request, group, meeting, items)
        if request.POST['ajax_button'][0:13] =='delete_button':
            delete_item(request, group, meeting)
        if request.POST['ajax_button'] == 'move_item':
            move_item(request, group, meeting)                          
        items = meeting.item_set.filter(group=group).order_by('item_no')
   
    item_formlist = []
    item_count = 0
    for item in items:
        item_count += 1
        item = AgendaForm(group, instance=item, prefix=item_count, label_suffix='')
        item_formlist.append(item)
    
    meeting_duration = get_formatted_meeting_duration(meeting_id)
#    meeting_end_time = calculate_meeting_end_time(meeting_id)
    
    if request_type == 'refresh':
        templates = ['agenda_edit.html']
    elif request_type == 'ajax':
        templates = ['agenda_edit_ajax_sidebar.html',
                     'agenda_edit_ajax_items.html']
    
    count = 0
    responses = []
    
    for template in templates:
        response = render(request, template, {
                          'meeting_id': meeting_id,
                          'meeting': meeting,
                          'meeting_duration': meeting_duration,
#                          'meeting_end_time': meeting_end_time,
                          'page_heading': page_heading,
                          'task_list_headings': task_list_headings,
                          'completed_tasks_list': completed_tasks_list,
                          'incomplete_tasks_list': incomplete_tasks_list,
                          'items': items,
                          'item_count': item_count,
                          'item_formlist': item_formlist,
                          'group': group,
                          'request_type': request_type,
                          })
        responses.append(response)
        
    if request_type == 'refresh':
        page_object = responses[0]
        return page_object
    elif request_type == 'ajax':
        ajax_response = {}
        ajax_sidebar_content = responses[0].content
        ajax_main_content = responses[1].content
        ajax_response['ajax_sidebar'] = ajax_sidebar_content
        ajax_response['ajax_main'] = ajax_main_content
        return HttpResponse(json.dumps(ajax_response), \
                            content_type="application/json")
      

def agenda_distribute(request, meeting_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))
    
    participants = Participant.objects.filter(group=group)
    pages = create_pdf_agenda(request, group, meeting)
    
    if request.method == "POST":
        if 'distribute_button' in request.POST:
            if request.POST['distribute_button']=='distribute_agenda':
            	distribute_agenda(request, group, meeting)
                return HttpResponseRedirect(reverse('agenda-sent',
                                                    args=(meeting_id)))
            	
    return render(request, 'agenda_distribute.html', {
                  'meeting_id': meeting_id,
                  'meeting': meeting,
                  'pages': pages,
                  'participants': participants,
                  })


def agenda_print(request, meeting_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    pdf_contents = get_pdf_contents(request, group, meeting)

    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=test-agenda.pdf'

    return response


def agenda_sent(request, meeting_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    page_heading = 'Agenda for meeting ' + meeting_id + ' sent.'
    
    return render(request, 'agenda_sent.html', {
                  'page_heading': page_heading,
                  })


def minutes_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    minutes = Meeting.objects.filter(group=group)
    page_heading = 'Minutes'
    table_headings = ('Meeting number', 'Date', 'Location',)
    
    return render(request, 'minutes_list.html', {
                  'minutes': minutes,
                  'page_heading': page_heading,
                  'table_headings': table_headings
                  })


def minutes_edit(request, meeting_id):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
        
    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))
    
    page_heading = 'Create minutes'
    task_list_headings = ('Description', 'Assigned to', 'Deadline')
        
    
    DecisionFormSet = inlineformset_factory(Meeting, Decision, extra=0, can_delete=True, widgets={'item': HiddenInput(), 'description': Textarea(attrs={'rows': 2}), 'owner': HiddenInput(),})
    TaskFormSet = inlineformset_factory(Meeting, Task, extra=0, can_delete=True, widgets={'item': HiddenInput(), 'status': HiddenInput(), 'owner': HiddenInput(), 'deadline': DateInput(attrs={'class': 'datepicker'}),})
    TaskFormSet.form.base_fields['participant'].queryset = Participant.objects.filter(owner=request.user)

    items = meeting.item_set.filter(owner=request.user).order_by('item_no')

    decision_items = meeting.decision_set.filter(owner=request.user)
    task_items = meeting.task_set.filter(owner=request.user)
    
    existing_data_forms = []
    request_type = 'refresh'
    
    decision_data_formset = DecisionFormSet(instance=meeting)				
    task_data_formset = TaskFormSet(instance=meeting)
    editable_section = 'is_main_items'
    
    incomplete_task_list = Task.objects.filter(owner=request.user, status="Incomplete")
    completed_task_list = Task.objects.filter(owner=request.user, status="Complete")
    account = Account.objects.filter(owner=request.user).last()
	
    def save_minutes_data(request, meeting):

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

       
        # Management of items 
        if 'edit_main_items_agenda_button' in request.POST:
            if request.POST['edit_main_items_agenda_button']=='edit_main_items':

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

                decision_data_formset = DecisionFormSet(instance=meeting)				
                task_data_formset = TaskFormSet(instance=meeting)				
                editable_section = 'is_main_items'	
	

    # Management of agenda items 
    if request.method == "POST" and 'ajax_button' in request.POST:

        request_type = 'ajax'
        
        if request.POST['ajax_button'] != 'page_refresh':              
            save_formset(request, meeting, items, 'minutes')
                
        if request.POST['ajax_button'][0:10]=='add_button':
            add_item(request, meeting_id, items)
        
        if request.POST['ajax_button'][0:13] =='delete_button':
            delete_item(request, meeting_id)
        
        if request.POST['ajax_button'] == 'move_item':
            move_item(request, meeting_id)
                              
        items = meeting.item_set.filter(owner=request.user).order_by('item_no')

    existing_data_forms = MeetingForm(instance=meeting, label_suffix='')
   
    item_formlist = []
    item_count = 0
    for item in items:
        item_count += 1
        item = MinutesForm(instance=item, prefix=item_count, label_suffix='')
        item_formlist.append(item)
    
    meeting_duration = get_formatted_meeting_duration(meeting_id)
    meeting_end_time = calculate_meeting_end_time(meeting_id)
    
    if request_type == 'refresh':
        templates = ['minutes_edit.html']
    elif request_type == 'ajax':
        templates = ['minutes_edit_ajax_sidebar.html',
                     'minutes_edit_ajax_items.html']
    
    count = 0
    responses = []
    
    for template in templates:
        response = render(request, template, {
                          'meeting_id': meeting_id,
                          'meeting': meeting,
                          'meeting_duration': meeting_duration,
                          'meeting_end_time': meeting_end_time,
                          'page_heading': page_heading,
                          'task_list_headings': task_list_headings,
                          'completed_task_list': completed_task_list,
                          'incomplete_task_list': incomplete_task_list,
                          'items': items,
                          'item_count': item_count,
                          'existing_data_forms': existing_data_forms,
                          'item_formlist': item_formlist,
                          'new_data_form': new_data_form,
                          'account': account,
                          'request_type': request_type,
                          'decision_items': decision_items,
                          'task_items': task_items,
                          'decision_data_formset': decision_data_formset,
                          'task_data_formset': task_data_formset,
                          })

        responses.append(response)
        
    if request_type == 'refresh':
        page_object = responses[0]
        return page_object
    elif request_type == 'ajax':
        ajax_response = {}
        ajax_sidebar_content = responses[0].content
        ajax_main_content = responses[1].content
        ajax_response['ajax_sidebar'] = ajax_sidebar_content
        ajax_response['ajax_main'] = ajax_main_content
        return HttpResponse(json.dumps(ajax_response), \
                            content_type="application/json")

