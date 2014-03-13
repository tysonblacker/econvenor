from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from docs.models import Item
from meetings.models import Meeting
from meetings.forms import AgendaMeetingForm
from utilities.commonutils import get_current_group


def meeting_add(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
    
    page_heading = 'Create agenda'

    if request.method == "POST":
        meeting_form = AgendaMeetingForm(group, request.POST)
        if meeting_form.is_valid() :
            # save the data
            meeting = meeting_form.save(group)
            # create a blank first agenda item and link it to the meeting
            first_item = Item(title='New item', item_no=1, group=group)
            meeting.item_set.add(first_item)
            # get the meeting id to enable the page redirect
            meeting_id = meeting.id
            return HttpResponseRedirect(reverse('agenda-edit',
                                                args=(meeting_id,)))
    else:
        meeting_form = AgendaMeetingForm(group)
            
    return render(request, 'meeting_add.html', {
                  'meeting_form': meeting_form,
                  'page_heading': page_heading
                  })
