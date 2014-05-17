import json
import os
import string
from datetime import date, datetime, timedelta

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from decisions.forms import MinutesDecisionForm
from decisions.models import Decision
from docs.forms import AgendaItemForm, MinutesItemForm
from docs.models import Item
from meetings.forms import AgendaMeetingForm, \
                           MinutesMeetingForm, \
                           NextMeetingForm
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
    item_number = int(item_number)
    predecessors = Decision.objects.filter(item_id=item_number)
    no_of_precessors = predecessors.count()
    new_decision_number = no_of_precessors + 1
    new_decision = Decision(item_id=item_number, group=group, meeting=meeting,
                            decision_no=new_decision_number, status = 'Draft')
    new_decision.save(group)


def add_task(request, group, meeting):
    """
    Adds a task to a minutes item.
    """
    item_number = request.POST['ajax_button'][9:]
    item_number = int(item_number)
    predecessors = Task.objects.filter(item_id=item_number)
    no_of_precessors = predecessors.count()
    new_task_number = no_of_precessors + 1
    new_task = Task(item_id=int(item_number), group=group, meeting=meeting,
                    task_no=new_task_number, status = 'Draft')
    new_task.save(group)


def delete_item(request, group, meeting, **kwargs):
    """
    Deletes an agenda item.
    """    
    if kwargs:
        item_number = kwargs['item_no']
        item_number = int(item_number)
    else:
        button_value = request.POST['ajax_button']
        item_number = int(button_value[12:])
    item = Item.objects.get(meeting=meeting, item_no=item_number, group=group)
    item.delete()
    if not kwargs:
        items = Item.objects.filter(meeting=meeting, group=group)
        for item in items:
            if item.item_no > item_number:
                new_item_number = item.item_no - 1
                item.item_no = new_item_number
                item.save()


def delete_decision(request, group, meeting, **kwargs):
    """
    Deletes a decision from a minutes item. If a decision number is passed via
    **kwargs then it is used, otherwise the decision number is found from the
    request.POST data
    """    
    # Get the decision
    if kwargs:
        decision_id = kwargs['decision_id']
    else:
        button_value = request.POST['ajax_button']
        decision_id = int(button_value[16:])
    decision = Decision.objects.get(meeting=meeting, group=group,
                                    id=decision_id)
    # Work out where the decision fitted with the item it was attached to
    deleted_decision_no = decision.decision_no
    item = decision.item
    # Delete the decision
    decision.delete()
    # Renumber other decisions on that item to fill the gap it left
    decisions = Decision.objects.filter(meeting=meeting, group=group,
                                        item=item)
    for decision in decisions:
        current_decision_no = decision.decision_no
        if current_decision_no > deleted_decision_no:
            new_decision_no = current_decision_no - 1
            decision.decision_no = new_decision_no
            decision.save()
                

def delete_task(request, group, meeting, **kwargs):
    """
    Deletes a task from a minutes item. If a task number is passed via
    **kwargs then it is used, otherwise the task number is found from the
    request.POST data
    """    
    # Get the task
    if kwargs:
        task_id = kwargs['task_id']
    else:
        button_value = request.POST['ajax_button']
        task_id = int(button_value[12:])
    task = Task.objects.get(meeting=meeting, group=group,
                                    id=task_id)
    # Work out where the task fitted with the item it was attached to
    deleted_task_no = task.task_no
    item = task.item
    # Delete the decision
    task.delete()
    # Renumber other decisions on that item to fill the gap it left
    tasks = Task.objects.filter(meeting=meeting, group=group,
                                item=item)
    for task in tasks:
        current_task_no = task.task_no
        if current_task_no > deleted_task_no:
            new_task_no = current_task_no - 1
            task.task_no = new_task_no
            task.save()

    
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
        

def save_meeting_form(request, group, meeting, doc_type):            
    """
    Saves the meeting form.
    """
    if doc_type == 'agenda':
        meeting_form = AgendaMeetingForm(group, request.POST, instance=meeting)
    elif doc_type == 'minutes':
        meeting_form = MinutesMeetingForm(group, request.POST, instance=meeting)        
    if meeting_form.is_valid():
        meeting_form.save(group)
    if doc_type == 'agenda':
        return meeting_form


def save_next_meeting_form(request, group, meeting):            
    """
    Saves the next meeting form.
    """
    next_meeting_form = NextMeetingForm(group, request.POST, 
                                        instance=meeting)        
    if next_meeting_form.is_valid():
        next_meeting_form.save(group)


def clear_minutes(request, group, meeting, decisions, items, tasks):
    """
    Deletes a set of minutes.
    """
    for decision in decisions:
        decision_id = decision.id
        delete_decision(request, group, meeting,
                        decision_id=decision_id)
    for task in tasks:
        task_id = task.id
        delete_task(request, group, meeting, task_id=task_id)    
    for item in items:
        if item.minute_notes:
            item.minute_notes = ''
            item.save()
        if item.added_in_meeting == True:
            item_no = item.item_no
            delete_item(request, group, meeting, item_no=item_no)
    meeting.status = 'Scheduled'
    meeting.apologies = ''
    meeting.attendance = ''
    meeting.date_actual = None
    meeting.start_time_actual = None
    meeting.end_time_actual = None
    meeting.facilitator_actual = None
    meeting.minute_taker_actual = None
    meeting.location_actual = ''
    meeting.instructions_actual = ''
    meeting.next_meeting_date = None
    meeting.next_meeting_facilitator = None
    meeting.next_meeting_instructions = ''
    meeting.next_meeting_location = ''
    meeting.next_meeting_minute_taker = None
    meeting.next_meeting_start_time = None
    meeting.save()

            
def calculate_meeting_duration(meeting):
    """
    Returns the duration of a meeting. If any item durations are zero,
    return a meeting duration of zero.
    """
    duration = 0
    items = Item.objects.filter(meeting=meeting)
    for item in items:
        if item.time_limit == None or item.time_limit == 0:
            duration = 0
            break
        duration += item.time_limit
    return duration
	

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
	
	
def get_formatted_meeting_duration(meeting):
    """
    Returns the duration of the meeting in hr:min format.
    """
    duration = calculate_meeting_duration(meeting)
    hours = duration / 60
    minutes = duration % 60
    if hours == 0:
	    formatted_duration = '%s mins (approx.)' % minutes
    elif hours == 1:
	    formatted_duration = '%s hr %s mins (approx.)' % (hours, minutes)	
    else:
	    formatted_duration = '%s hrs %s mins (approx.)' % (hours, minutes)
    return formatted_duration
	

def get_overdue_tasks_list(group, meeting, doc_type):
    """
    Return overdue tasks for agendas and minutes.
    """
    today = date.today()
    if doc_type == "agenda":
        meeting_date = meeting.date_scheduled
        # If today's date is before the scheduled meeting date,
        # return a list of tasks currently overdue.
        if meeting_date > today:
            tasks_list = Task.lists.overdue_tasks().filter(group=group)  
    elif doc_type == "minutes":        
        meeting_date = meeting.date_actual
        # If today's date is before the actual meeting date,
        # return an empty list.
        if meeting_date > today:
            tasks_list = []
    # If today is on or after the meeting date, return a list of tasks
    # which were overdue on the actual meeting date.
    if meeting_date <= today:
        # 1.Exclude tasks with status cancelled or draft
        # 2.Only allow tasks due before/on the meeting date
        # 3.Exclude tasks completed before/on the meeting date
        tasks_list = Task.objects.filter(group=group).\
                     filter(status__in=['Completed', 'Incomplete']).\
                     filter(deadline__lt=meeting_date).\
                     exclude(completion_date__lte=meeting_date).\
                     order_by('deadline')
    return tasks_list


def get_outstanding_tasks_list(group, meeting, doc_type):
    """
    Return outstanding tasks for agendas and minutes.
    """
    today = date.today()
    if doc_type == "agenda":
        meeting_date = meeting.date_scheduled
        # If today's date is before the scheduled meeting date,
        # return a list of tasks currently outstanding.
        if meeting_date > today:
            tasks_list = Task.lists.pending_tasks().filter(group=group)
    elif doc_type == "minutes":        
        meeting_date = meeting.date_actual
        # If today's date is before the actual meeting date,
        # return an empty list.
        if meeting_date > today:
            tasks_list = []
    # If today is on or after the meeting date, return a list of tasks
    # which were outstanding on the meeting date.
    if meeting_date <= today:
        # Because meeting_date is a date() and it will be compared with a 
        # datetime() in the query following, day_following_meeting is needed
        # for the queryset to evaluate to the correct result.
        day_after_meeting = meeting_date + timedelta(1)
        # 1.Exclude tasks with status cancelled or draft
        # 2.Only allow tasks created before/on the meeting date, or else tasks
        #   created after the meeting and before minutes are made will appear.
        # 3.Exclude tasks tasks due before the meeting date
        # 4.Exclude tasks completed before/on the meeting date
        tasks_list = Task.objects.filter(group=group).\
                     filter(status__in=['Completed', 'Incomplete']).\
                     filter(created__lt=day_after_meeting).\
                     exclude(deadline__lt=meeting_date).\
                     exclude(completion_date__lte=meeting_date).\
                     order_by('deadline')
    return tasks_list


def get_completed_tasks_list(group, meeting, doc_type):
    """
    Return completed tasks for agendas and minutes.
    """
    # Find the preceding meeting date, if there is one
    meetings = Meeting.objects.filter(group=group, meeting_status='Completed')
    if meetings:
        preceding_meeting = meetings.order_by('date_actual').last()
        previous_mtg_date = preceding_meeting.date_actual
    else:
        previous_mtg_date = None
    # Set the meeting_date variable
    if doc_type == "agenda":
        meeting_date = meeting.date_scheduled
    elif doc_type == "minutes":
        meeting_date = meeting.date_actual
    # Generate the completed task list if there is a previous meeting
    if previous_mtg_date != None:
        # 1.Only allow tasks completed after the previous meeting date
        # 2.Exclude tasks completed after the meeting date
        completed_task_list = Task.lists.completed_tasks().\
                              filter(group=group).\
                              filter(completion_date__gt=previous_mtg_date).\
                              exclude(completion_date__gt=meeting_date).\
                              order_by('deadline')                              
    # Generate the completed task list if there is no previous meeting
    elif previous_mtg_date == None:
        # 1.Allow all tasks completed before the meeting date
        completed_task_list = Task.lists.completed_tasks().\
                              filter(group=group).\
                              filter(completion_date__lte=meeting_date).\
                              order_by('deadline')                              
    return completed_task_list


def get_templates(request_type, doc_type):
    """
    Returns the templates required to render the response
    for an agenda or minutes.
    """    
    if request_type == 'refresh':
        templates = ['document_edit.html']
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

def undraft_tasks_and_decisions(group, meeting):
    """
    Changes the status of tasks and decisions attached to minutes from draft to
    distributed once the minutes are sent out.
    """      
    decisions = meeting.decision_set.filter(group=group)
    tasks = meeting.task_set.filter(group=group)
    for decision in decisions:
        decision.status = 'Distributed'
        decision.save()    
    for task in tasks:
        task.status = 'Incomplete'
        task.save()    


def populate_minutes_meeting_details(group, meeting):
    """
    In minutes have not yet been distributed, populates the meeting details
    form of the minutes edit view with corresponding data from the agenda.
    """      
    if not meeting.current_minutes_version:
        meeting.date_actual = meeting.date_scheduled
        meeting.start_time_actual = meeting.start_time_scheduled
        meeting.location_actual = meeting.location_scheduled
        meeting.facilitator_actual = meeting.facilitator_scheduled        
        meeting.minute_taker_actual = meeting.minute_taker_scheduled
        meeting.save()
