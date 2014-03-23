from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from docs.models import Item
from meetings.forms import AgendaMeetingForm
from meetings.models import Meeting
from meetings.utils import archive_meeting, delete_meeting
from utilities.commonutils import get_current_group


def meeting_add(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

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

    menu = {'parent': 'meetings', 'child': 'new_meeting'}            
    return render(request, 'meeting_add.html', {
                  'menu': menu,
                  'meeting_form': meeting_form,
                  })
                  

def meeting_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))
            
    meetings = Meeting.lists.current_meetings().filter(group=group)
    table_headings = ('Date',
                      'Meeting Number',
                      'Agenda sent',
                      'Minutes sent',
                      'Next action',
                      '',
                      )

    if request.method == "POST":
        if request.POST['button'][:6] == 'delete':           
            delete_meeting(request, group)
        if request.POST['button'][:7] == 'archive':           
            archive_meeting(request, group)
        meetings = Meeting.lists.current_meetings().filter(group=group)
                        
    menu = {'parent': 'meetings', 'child': 'all_meetings'}    
    return render(request, 'meeting_list.html', {
                  'menu': menu,
                  'meetings': meetings,
                  'table_headings': table_headings
                  })
    
