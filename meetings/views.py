from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from docs.models import Item
from meetings.models import Meeting
from meetings.forms import AddMeetingForm, AddMeetingDetailsForm
from meetings.utils import create_first_item
from utilities.commonutils import get_current_group


def meeting_add(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    
    page_heading = 'Create agenda'

    if request.method == "POST":
        meeting_form = AddMeetingForm(group, request.POST)
        meeting_details_form = AddMeetingDetailsForm(group, request.POST)
        if meeting_form.is_valid() and meeting_details_form.is_valid():
            # save the data
            m = meeting_form.save(group)
            md = meeting_details_form.save(group)            
            # link the scheduled meeting details to the meeting
            m.meetingdetails_set.add(md) 
            # create a blank first agenda item and link it to the meeting
            first_item = Item(title='New item', item_no=1, group=group)
            m.item_set.add(first_item)
            # get the meeting id to enable the page redirect
            meeting_id = m.id
            return HttpResponseRedirect(reverse('agenda-edit',
                                                args=(meeting_id,)))
    else:
        meeting_form = AddMeetingForm(group)
        meeting_details_form = AddMeetingDetailsForm(group)
            
    return render(request, 'meeting_add.html', {
                  'meeting_form': meeting_form,
                  'meeting_details_form': meeting_details_form,                  
                  'page_heading': page_heading
                  })
