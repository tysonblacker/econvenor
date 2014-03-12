import json

from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.forms import DateInput, HiddenInput, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from accounts.models import Group
from decisions.models import Decision
from docs.forms import AgendaItemForm, MinutesItemForm
from docs.models import Item
from docs.pdfs import create_pdf_agenda, \
                      get_pdf_contents
from docs.utils import add_item, \
                       build_formlist, \
                       calculate_meeting_duration, \
                       calculate_meeting_end_time, \
                       delete_item, \
                       distribute_agenda, \
                       get_completed_tasks_list, \
                       get_formatted_meeting_duration, \
                       move_item, \
                       save_formlist
from meetings.models import Meeting
from meetings.forms import MinutesMeetingForm
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
  
    incomplete_tasks_list = Task.lists.incomplete_tasks().filter(group=group)
    completed_tasks_list = get_completed_tasks_list(group=group)

    if request.method == "POST" and 'ajax_button' in request.POST:
        request_type = 'ajax'
        if request.POST['ajax_button'] != 'page_refresh':              
            save_formlist(request, group, items, 'items', 'agenda')
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
        item = AgendaItemForm(group, instance=item,
                          prefix=item_count, label_suffix='')
        item_formlist.append(item)
    
    meeting_duration = get_formatted_meeting_duration(meeting_id)
    meeting_end_time = calculate_meeting_end_time(meeting)
    
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
                          'meeting_end_time': meeting_end_time,
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
    table_headings = ('Meeting ID', 'Meeting number', 'Date of meeting',)
    
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
    
    request_type = 'refresh'
    page_heading = 'Minutes'
    task_list_headings = ('Description', 'Assigned to', 'Deadline')
    
    items = meeting.item_set.filter(group=group).order_by('item_no')
    decisions = meeting.decision_set.filter(group=group)
    tasks = meeting.task_set.filter(group=group)
    
    incomplete_tasks_list = Task.lists.incomplete_tasks().filter(group=group)
    completed_tasks_list = get_completed_tasks_list(group=group)
    new_tasks = Task.lists.incomplete_tasks().filter(group=group,
                                                     meeting=meeting)	

    if request.method == "POST" and 'ajax_button' in request.POST:
        request_type = 'ajax'
        if request.POST['ajax_button'] != 'page_refresh':              
            save_formlist(request, group, items, 'items', 'minutes')
            save_formlist(request, group, tasks, 'tasks', 'minutes')            
            save_formlist(request, group, decisions, 'decisions',
                          'minutes')            
        if request.POST['ajax_button']=='add_item_button':
            add_item(request, group, meeting, items)
        if request.POST['ajax_button'][:15]=='add_task_button':
            item_number = request.POST['ajax_button'][16:]
            new_task = Task(item_id=int(item_number), meeting=meeting,
                            status = 'Incomplete')
            new_task.save(group)
        if request.POST['ajax_button'][:19]=='add_decision_button':
            item_number = request.POST['ajax_button'][20:]
            new_decision = Decision(item_id=int(item_number), meeting=meeting)
            new_decision.save(group)
        
        items = meeting.item_set.filter(group=group).order_by('item_no')
        tasks = meeting.task_set.filter(group=group)
        decisions = meeting.decision_set.filter(group=group)
   
    item_formlist = build_formlist(group, items, 'items', 'minutes')
    task_formlist = build_formlist(group, tasks, 'tasks', 'minutes')
    decision_formlist = build_formlist(group, decisions, 'decisions',
                                       'minutes')    
    
    item_count = items.count()
    meeting_form = MinutesMeetingForm(group, instance=meeting, label_suffix='') 
    meeting_duration = get_formatted_meeting_duration(meeting_id)
    meeting_end_time = calculate_meeting_end_time(meeting)
    
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
                          'completed_tasks_list': completed_tasks_list,
                          'incomplete_tasks_list': incomplete_tasks_list,
                          'item_count': item_count,
                          'meeting_form': meeting_form,
                          'item_formlist': item_formlist,
                          'task_formlist': task_formlist,
                          'decision_formlist': decision_formlist,
                          'request_type': request_type,
                          'decisions': decisions,
                          'tasks': tasks,
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

