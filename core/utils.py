from core.models import Item, Meeting


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
			
