from core.models import Item


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
