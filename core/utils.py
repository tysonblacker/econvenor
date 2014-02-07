from core.models import Item, Meeting

import markdown
import socket

from datetime import datetime, timedelta

def save_and_add_owner(request, form_object):
	form = form_object
	if form.is_valid():
		temp_form = form.save(commit=False)
		temp_form.owner = request.user
		temp_form.save()
	
		
def calculate_meeting_duration(meeting_id):
	duration = 0
	items = Item.objects.filter(meeting=meeting_id)
	for item in items:
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


def convert_markdown_to_html(mkd_file):
	f = open(mkd_file, "r")
	mkd_content = f.read()
	html_content = markdown.markdown(mkd_content)
	f.close()
	return html_content


def set_path(local_path, server_path):
	if socket.gethostname() == 'web439.webfaction.com':
		FONT_PATH = server_path
	else:
		FONT_PATH = local_path
	return FONT_PATH
	

