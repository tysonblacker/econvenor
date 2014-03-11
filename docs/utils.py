import os
import string

from datetime import datetime, timedelta
from django.core.mail import EmailMessage

from django.conf import settings

from docs.forms import AgendaForm, MinutesForm
from docs.models import Item
from meetings.models import Meeting
from participants.models import Participant
from tasks.models import Task
from utilities.commonutils import set_path


def delete_item(request, group, meeting):
    """
    Deletes an agenda item.
    """    
    button_value = request.POST['ajax_button']
    item_number = int(button_value[14:])
    item = Item.objects.get(meeting=meeting, item_no=item_number, group=group)
    item.delete()
    items = Item.objects.filter(meeting=meeting, group=group)
    
    for item in items:
        if item.item_no > item_number:
            new_item_number = item.item_no - 1
            item.item_no = new_item_number
            item.save()


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
   

def add_item(request, group, meeting, items):
    """
    Adds an agenda item. Requires *items* to be a list of items ordered
    from first to last.
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
    new_item.save()


def save_formlist(request, group, meeting, items, doc_type):
    """
    Saves the agenda items for the agenda currently being edited.
    """

    updated_formlist = []
    count = 1
    for item in items:
        if doc_type == 'agenda':
            updated_item = AgendaForm(group, request.POST,
                                      prefix=count, instance=item)
        if doc_type == 'minutes':
            updated_item = MinutesForm(group, request.POST,
                                       prefix=count, instance=item)
        if updated_item.is_valid():
            updated_item.save(group)
        updated_formlist.append(updated_item)
        count += 1
    
    
def calculate_meeting_duration(meeting):
	duration = 0
	items = Item.objects.filter(meeting=meeting)
	for item in items:
	    if item.time_limit:
		    duration += item.time_limit
	return duration
	
	
def get_formatted_meeting_duration(meeting_id):
	duration = calculate_meeting_duration(meeting_id)
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
	duration = calculate_meeting_duration(meeting)
	date = meeting.date_scheduled
	start_time = meeting.start_time_scheduled
	start_date_and_time = datetime.combine(date, start_time)
	end_date_and_time = start_date_and_time + timedelta(minutes=duration)
	end_time = end_date_and_time.time()
	return end_time
	

def get_completed_tasks_list(group):
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


def distribute_agenda(request, group, meeting):
	
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
