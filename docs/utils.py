import json
import os
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect

from decisions.forms import MinutesDecisionForm
from decisions.models import Decision
from docs.forms import AgendaItemForm, MinutesItemForm
from docs.models import Item
from meetings.models import Meeting
from participants.models import Participant
from tasks.forms import MinutesTaskForm
from tasks.models import Task
from utilities.commonutils import set_path


def add_item(group, meeting, items, doc_type):
    """
    Adds an agenda or minutes item. Requires *items* to be a list of items
    ordered from first to last.
    """
    try:
        last_item = items.reverse()[0]
        last_item_no = last_item.item_no
    except:
        last_item_no = 0

    new_item_no = last_item_no + 1 
    new_item = Item(item_no=new_item_no,
               meeting=meeting,
               group=group,
               title='New item'
               )
    if doc_type == 'minutes':
        new_item.added_in_meeting = True
    new_item.save(group)


def add_decision(request, group, meeting):
    """
    Adds a decision to a minutes item.
    """
    item_number = request.POST['ajax_button'][13:]
    new_decision = Decision(item_id=int(item_number), group=group,
                            meeting=meeting)
    new_decision.save(group)


def add_task(request, group, meeting):
    """
    Adds a task to a minutes item.
    """
    item_number = request.POST['ajax_button'][9:]
    new_task = Task(item_id=int(item_number), group=group,              
                    meeting=meeting, status = 'Incomplete')
    new_task.save(group)


def delete_item(request, group, meeting):
    """
    Deletes an agenda item.
    """    
    button_value = request.POST['ajax_button']
    item_number = int(button_value[12:])
    item = Item.objects.get(meeting=meeting, item_no=item_number, group=group)
    item.delete()
    items = Item.objects.filter(meeting=meeting, group=group)
    
    for item in items:
        if item.item_no > item_number:
            new_item_number = item.item_no - 1
            item.item_no = new_item_number
            item.save()


def delete_decision(request, group, meeting):
    """
    Deletes a decision from a minutes item.
    """    
    button_value = request.POST['ajax_button']
    decision_number = int(button_value[16:])
    decision = Decision.objects.get(meeting=meeting, group=group,
                                    id=decision_number)
    decision.delete()


def delete_task(request, group, meeting):
    """
    Deletes a task from a minutes item.
    """    
    button_value = request.POST['ajax_button']
    task_number = int(button_value[12:])
    task = Task.objects.get(meeting=meeting, group=group,
                                    id=task_number)
    task.delete()
    
    
def move_item(request, group, meeting):
    """
    Moves an agenda item relative to other agenda items.
    """   
    ajax_data = request.POST['new_sidebar_order']
    ajax_data_list = string.split(ajax_data, ',')

    last_item = 0
    count = 0
    moved_item = None
    
    for item in ajax_data_list:
        item = int(item)
        difference = item - last_item
        if difference == 2:
            moved_item = (item+last_item)/2
            break
        last_item = item
        count += 1
    
    if moved_item == None:
        moved_item = count
    
    old_position = moved_item

    position = 1
    for item in ajax_data_list:
        item = int(item)
        if item == moved_item:
            new_position = position
            break
        position += 1
          
    items = Item.objects.filter(meeting=meeting, group=group)
    
    for item in items:
        if item.item_no == moved_item:
            item.item_no = new_position
            item.save()
        elif old_position < new_position: # the item has moved down the list
            if item.item_no <= new_position and item.item_no > old_position:
                new_item_number = item.item_no - 1
                item.item_no = new_item_number
                item.save()
        elif old_position > new_position: # the item has moved up the list
            if item.item_no >= new_position and item.item_no < old_position:
                new_item_number = item.item_no + 1
                item.item_no = new_item_number
                item.save()
   

def build_formlist(group, items, item_type, doc_type):
    """
    Builds and returns a populated formlist.
    """
    formlist = []
    count = 0
    for item in items:
        count += 1
        if item_type == 'items':
            prefix = 'i' + str(count)
        elif item_type == 'tasks':
            prefix = 't' + str(count)
        elif item_type == 'decisions':
            prefix = 'd' + str(count)           
        if doc_type == 'agenda':
            formlist_item = AgendaItemForm(group, prefix=prefix, instance=item, 
                                          label_suffix='')
        elif doc_type == 'minutes':
            if item_type == 'items':
                formlist_item = MinutesItemForm(group, prefix=prefix,
                                               instance=item, label_suffix='')
            if item_type == 'tasks':
                formlist_item = MinutesTaskForm(group, prefix=prefix,
                                               instance=item, label_suffix='')
            if item_type == 'decisions':
                formlist_item = MinutesDecisionForm(group, prefix=prefix, 
                                                   instance=item, 
                                                   label_suffix='')
        formlist.append(formlist_item)

    return formlist


def save_formlist(request, group, items, item_type, doc_type):
    """
    Saves all forms in a formlist.
    """
    count = 0
    for item in items:
        count += 1
        if item_type == 'items':
            prefix = 'i' + str(count)
        elif item_type == 'tasks':
            prefix = 't' + str(count)
        elif item_type == 'decisions':
            prefix = 'd' + str(count)           

        if doc_type == 'agenda':
            updated_item = AgendaItemForm(group, request.POST,
                                          prefix=prefix, instance=item,
                                          label_suffix='')
        elif doc_type == 'minutes':
            if item_type == 'items':
                updated_item = MinutesItemForm(group, request.POST,
                                              prefix=prefix, instance=item,
                                              label_suffix='')
            if item_type == 'tasks':
                updated_item = MinutesTaskForm(group, request.POST,
                                               prefix=prefix, instance=item,
                                               label_suffix='')
            if item_type == 'decisions':
                updated_item = MinutesDecisionForm(group, request.POST,
                                                   prefix=prefix,instance=item,
                                                   label_suffix='')
        if updated_item.is_valid():
            updated_item.save(group)
        

def calculate_meeting_duration(meeting):
    """
    Returns the duration of a meeting.
    """
    duration = 0
    items = Item.objects.filter(meeting=meeting)
    for item in items:
        if item.time_limit:
            duration += item.time_limit
    return duration
	
	
def get_formatted_meeting_duration(meeting):
    """
    Returns the duration of the meeting in hr:min format.
    """
    duration = calculate_meeting_duration(meeting)
    hours = duration / 60
    minutes = duration % 60
    if hours == 0:
	    formatted_duration = '%s mins' % minutes
    elif hours == 1:
	    formatted_duration = '%s hr %s mins' % (hours, minutes)	
    else:
	    formatted_duration = '%s hrs %s mins' % (hours, minutes)
    return formatted_duration
	

def calculate_meeting_end_time(meeting):
    """
    Returns the end time of a meeting.
    """
    duration = calculate_meeting_duration(meeting)
    date = meeting.date_scheduled
    start_time = meeting.start_time_scheduled
    start_date_and_time = datetime.combine(date, start_time)
    end_date_and_time = start_date_and_time + timedelta(minutes=duration)
    end_time = end_date_and_time.time()
    return end_time
	

def get_completed_tasks_list(group):
    """
    Returns a list of tasks completed since the last meeting.
    """
    meetings = Meeting.objects.filter(group=group, meeting_status='Complete',
                                      meeting_type='Ordinary Meeting')
    if meetings:
        preceding_meeting = meetings.order_by('date_actual').last()
        preceding_meeting_date = preceding_meeting.date_actual
    else:
        preceding_meeting_date = None

    completed_task_list = []
    if preceding_meeting_date != None:
        completed_task_list = Task.lists.complete_tasks.filter(group=group,
            deadline__gte=preceding_meeting_date)

    return completed_task_list


def get_templates(request_type, doc_type):
    """
    Returns the templates required to render the response
    for an agenda or minutes.
    """    
    if request_type == 'refresh':
        if doc_type == 'agenda':
            templates = ['agenda_edit.html']
        elif doc_type == 'minutes':
            templates = ['minutes_edit.html']
    elif request_type == 'ajax':
        if doc_type == 'agenda':
            templates = ['agenda_edit_ajax_sidebar.html',
                         'agenda_edit_ajax_items.html']
        elif doc_type == 'minutes':
            templates = ['minutes_edit_ajax_sidebar.html',
                         'minutes_edit_ajax_items.html']
    return templates


def get_response(responses, request_type):
    """
    Returns the response for an agenda or minutes.
    """      
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


def distribute_agenda(request, group, meeting):
    """
    Emails out the agenda.
    """  	
    recipients = []
    group_name = group.name
        
    # build recipients list if "all_participants" box is checked
    if 'all_participants' in request.POST:
	    participants = Participant.objects.filter(group=group)
	    for participant in participants:
		    email = participant.email
		    recipients.append(email)
		
    # build recipients list if "all_participants" box is not checked
    else:
	    # create recipients list in this format: [participant1, participant4]
	    distribution_list = []
	    for key in request.POST:
		    if request.POST[key] == 'checked':
			    distribution_list.append(key)

	    # create recipients list in this format: [1, 4]
	    id_list = []
	    for participant in distribution_list:
		    participant_id = participant[11:]
		    id_list.append(participant_id)

	    # create recipients list with email addresses

	    for item in id_list:
		    participant = Participant.objects.get(pk=int(item), group=group)
		    participant_email = participant.email
		    recipients.append(participant_email)

    # set up the email fields
    pdf_path = os.path.join(settings.BASE_DIR, meeting.agenda_pdf.url[1:])	
    subject = group_name + ': You agenda is attached'
    body = 'Here is your agenda'
    sender = 'noreply@econvenor.org'

    # email the agenda
    email = EmailMessage(subject, body, sender, recipients)
    email.attach_file(pdf_path)
    email.send()
