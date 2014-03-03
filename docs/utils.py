import string

from docs.forms import AgendaForm, MinutesForm
from docs.models import Item
from meetings.models import Meeting
from participants.models import Participant
from datetime import datetime, timedelta
from django.core.mail import EmailMessage


def delete_item(request, meeting_id):
    button_value = request.POST['agenda_button']
    item_number = int(button_value[14:])
    item = Item.objects.get(meeting=meeting_id, item_no=item_number)
    item.delete()
    items = Item.objects.filter(meeting=meeting_id)
    for item in items:
        if item.item_no > item_number:
            new_item_number = item.item_no - 1
            item.item_no = new_item_number
            item.save()


def move_item(request, meeting_id):
    
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
          
    items = Item.objects.filter(meeting=meeting_id)
    
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
   

def add_item(request, meeting_number, items):
    """
    Requires *items* to be a list of items ordered from first to last
    """
    try:
        last_item = items.reverse()[0]
        last_item_no = last_item.item_no
    except:
        last_item_no = 0

    new_item_no = last_item_no + 1 
    new_item = Item(item_no=new_item_no,
                meeting_id=int(meeting_number),
                owner=request.user,
                heading='New item'
               )
    new_item.save()


def save_formset(request, meeting, items, doc_type):
    updated_formset = []
    count = 1
    for item in items:
        if doc_type == 'agenda':
            updated_item = AgendaForm(request.POST, prefix=count, instance=item)
        if doc_type == 'minutes':
            updated_item = MinutesForm(request.POST, prefix=count, instance=item)
        updated_formset.append(updated_item)
        count += 1
    for updated_item in updated_formset:
        item = updated_item.save(commit=False)
        item.owner = request.user
        item.editable = True
        item.meeting = meeting
        item.minute_notes = 'Changed by agenda refresh'
        item.show_tasks = False
        item.save()



def calculate_meeting_duration(meeting_id):
	duration = 0
	items = Item.objects.filter(meeting=meeting_id)
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
	

def calculate_meeting_end_time(meeting_id):
	meeting = Meeting.objects.get(pk=int(meeting_id))
	duration = calculate_meeting_duration(meeting_id)
	date = meeting.date
	start_time = meeting.start_time
	start_date_and_time = datetime.combine(date, start_time)
	end_date_and_time = start_date_and_time + timedelta(minutes=duration)
	end_time = end_date_and_time.time()
	return end_time
	

def find_preceding_meeting_date(user, meeting_id):
	meetings = Meeting.objects.filter(owner=user, description='Ordinary meeting' ).order_by('date').reverse()
	current_meeting = Meeting.objects.get(pk=int(meeting_id))
	current_meeting_date = current_meeting.date
	preceding_meeting_date = None
	for meeting in meetings:
		if current_meeting_date <= meeting.date:
			pass
		else:
			preceding_meeting_date = meeting.date
			break
	return preceding_meeting_date


def distribute_agenda(request, meeting_id, pdf):
	
	recipients = []
	group_name = get_group_name(request)
	
	# build recipients list if "all_participants" box is checked
	if 'all_participants' in request.POST:
		participants = Participant.objects.filter(owner=request.user)
		for participant in participants:
			participant_email_address = participant.email_address
			recipients.append(participant_email_address)
			
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
			participant = Participant.objects.get(pk=int(item))
			participant_email_address = participant.email_address
			recipients.append(participant_email_address)

	# set up the email fields
	file_name = 'Agenda' + str(meeting_id) + '.pdf'
	subject = group_name + ': ' + file_name + ' is attached'
	body = 'Here is ' + file_name
	sender = 'noreply@econvenor.org'

	# email the agenda
	email = EmailMessage(subject, body, sender, recipients)
	email.attach(file_name, pdf, 'application/pdf')
	email.send()
