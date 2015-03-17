from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from docs.pdfs import create_images_from_pdf, \
                      create_pdf, \
                      distribute_pdf, \
                      get_base_file_name, \
                      get_pdf_preview_contents
from docs.utils import add_decision, \
                       add_item, \
                       add_task, \
                       build_formlist, \
                       calculate_meeting_duration, \
                       calculate_meeting_end_time, \
                       clear_minutes, \
                       delete_decision, \
                       delete_item, \
                       delete_task, \
                       get_completed_tasks_list, \
                       get_formatted_meeting_duration, \
                       get_outstanding_tasks_list, \
                       get_overdue_tasks_list, \
                       get_response, \
                       get_templates, \
                       move_item, \
                       populate_minutes_meeting_details, \
                       save_formlist, \
                       save_meeting_form, \
                       save_next_meeting_form, \
                       undraft_tasks_and_decisions
from meetings.models import Meeting
from meetings.forms import AgendaMeetingForm, \
                           MinutesMeetingForm, \
                           NextMeetingForm
from meetings.utils import archive_meeting
from participants.models import Participant
from tasks.models import Task
from utilities.commonutils import get_current_group


def agenda_edit(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'agenda'
    request_type = 'refresh'
    task_list_headings = ('Description',
                          'Assigned to',
                          'Deadline')
    items = meeting.item_set.filter(group=group).order_by('item_no')
    overdue_tasks_list = get_overdue_tasks_list(group=group,
                                                meeting=meeting,
                                                doc_type=doc_type)
    pending_tasks_list = get_outstanding_tasks_list(group=group,
                                                    meeting=meeting,
                                                    doc_type=doc_type)
    completed_tasks_list = get_completed_tasks_list(group=group,
                                                    meeting=meeting,
                                                    doc_type=doc_type)

    if request.method == "POST" and 'ajax_button' in request.POST:
        request_type = 'ajax'
        if request.POST['ajax_button'] != 'page_refresh':
            save_formlist(request, group, items, 'items', doc_type)
            meeting_form = save_meeting_form(request, group, meeting, doc_type)
        if request.POST['ajax_button']=='add_item':
            add_item(group, meeting, items, doc_type)
        if request.POST['ajax_button'][0:11] =='delete_item':
            delete_item(request, group, meeting)
        if request.POST['ajax_button'] == 'move_item':
            move_item(request, group, meeting)
        items = meeting.item_set.filter(group=group).order_by('item_no')

    item_formlist = build_formlist(group, items, 'items', doc_type)

    meeting_form = AgendaMeetingForm(group=group, instance=meeting,
                                     label_suffix='')
    meeting_duration = get_formatted_meeting_duration(meeting_id)
    meeting_end_time = calculate_meeting_end_time(meeting)

    templates = get_templates(request_type, doc_type)
    responses = []
    menu = {'parent': 'meetings',
            'child': 'current_meetings',
            'tips': 'create_agenda'}
    for template in templates:
        part_response = render(request, template, {
                               'menu': menu,
                               'completed_tasks_list': completed_tasks_list,
                               'doc_type': doc_type,
                               'group': group,
                               'item_formlist': item_formlist,
                               'items': items,
                               'meeting': meeting,
                               'meeting_duration': meeting_duration,
                               'meeting_end_time': meeting_end_time,
                               'meeting_form': meeting_form,
                               'meeting_id': meeting_id,
                               'overdue_tasks_list': overdue_tasks_list,
                               'pending_tasks_list': pending_tasks_list,
                               'task_list_headings': task_list_headings,
                               })
        responses.append(part_response)
    response = get_response(responses, request_type)

    return response


def agenda_distribute(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'agenda'
    participants = Participant.lists.active().filter(group=group)
    pages = create_pdf(request, group, meeting, doc_type)

    if request.method == "POST":
        if 'distribute_button' in request.POST:
            if request.POST['distribute_button']=='distribute':
                distribute_pdf(request, group, meeting, doc_type)
                populate_minutes_meeting_details(group, meeting)
                return HttpResponseRedirect(reverse('agenda-sent',
                                                    args=(meeting_id,)))

    menu = {'parent': 'meetings',
            'child': 'current_meetings',
            'tips': 'review_agenda'}
    return render(request, 'document_distribute.html', {
                  'menu': menu,
                  'doc_type': doc_type,
                  'meeting_id': meeting_id,
                  'pages': pages,
                  'participants': participants,
                  })


def agenda_print(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    pdf_contents = get_pdf_preview_contents(request, group, meeting, 'agenda')
    file_name = group.slug + '_agenda_' + meeting.meeting_no + '.pdf'

    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name

    return response


def agenda_sent(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'agenda'
    meeting_no = meeting.meeting_no

    menu = {'parent': 'meetings'}
    return render(request, 'document_sent.html', {
                  'menu': menu,
                  'meeting_no': meeting_no,
                  'doc_type': doc_type,
                  })


def agenda_view(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'agenda'
    version = meeting.current_agenda_version
    base_file_name = get_base_file_name(request, group, meeting, 'agenda')
    pages = create_images_from_pdf(base_file_name, version=version)

    menu = {'parent': 'meetings'}
    return render(request, 'document_view.html', {
                  'menu': menu,
                  'doc_type': doc_type,
                  'meeting_id': meeting_id,
                  'pages': pages,
                  })


def minutes_edit(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'minutes'
    request_type = 'refresh'

    decisions = meeting.decision_set.filter(group=group).\
                order_by('item', 'decision_no')
    items = meeting.item_set.filter(group=group).order_by('item_no')
    tasks = meeting.task_set.filter(group=group).\
            order_by('item', 'task_no')

    completed_tasks_list = get_completed_tasks_list(group=group,
                                                    meeting=meeting,
                                                    doc_type='minutes')
    incomplete_tasks_list = Task.lists.incomplete_tasks().filter(group=group)
    new_tasks = Task.lists.incomplete_tasks().filter(group=group,
                                                     meeting=meeting)

    if request.method == "POST" and 'ajax_button' in request.POST:
        request_type = 'ajax'
        # before changing any data, save everything
        if request.POST['ajax_button'] != 'page_refresh':
            save_formlist(request, group, decisions, 'decisions', doc_type)
            save_formlist(request, group, items, 'items', doc_type)
            save_formlist(request, group, tasks, 'tasks', doc_type)
            save_meeting_form(request, group, meeting, doc_type)
            save_next_meeting_form(request, group, meeting)
        # now change what needs to be changed
        if request.POST['ajax_button']=='clear_minutes':
            clear_minutes(request, group, meeting, decisions, items, tasks)
        if request.POST['ajax_button'][:12]=='add_decision':
            add_decision(request, group, meeting)
        if request.POST['ajax_button']=='add_item':
            add_item(group, meeting, items, 'minutes')
        if request.POST['ajax_button'][:8]=='add_task':
            add_task(request, group, meeting)
        if request.POST['ajax_button'][:15]=='delete_decision':
            delete_decision(request, group, meeting)
        if request.POST['ajax_button'][:11]=='delete_item':
            delete_item(request, group, meeting)
        if request.POST['ajax_button'][:11]=='delete_task':
            delete_task(request, group, meeting)

        decisions = meeting.decision_set.filter(group=group).\
                    order_by('item', 'decision_no')
        items = meeting.item_set.filter(group=group).order_by('item_no')
        tasks = meeting.task_set.filter(group=group).\
                order_by('item', 'task_no')

    decision_formlist = build_formlist(group, decisions, 'decisions',
                                       'minutes')
    item_formlist = build_formlist(group, items, 'items', 'minutes')
    task_formlist = build_formlist(group, tasks, 'tasks', 'minutes')

    item_count = items.count()
    meeting_duration = get_formatted_meeting_duration(meeting)
    meeting_end_time = calculate_meeting_end_time(meeting)
    meeting_form = MinutesMeetingForm(group, instance=meeting, label_suffix='')
    next_meeting_form = NextMeetingForm(group, instance=meeting,
                                        label_suffix='')
    templates = get_templates(request_type, 'minutes')
    responses = []
    menu = {'parent': 'meetings',
            'child': 'current_meetings',
            'tips': 'create_minutes'}
    for template in templates:
        response = render(request, template, {
                          'menu': menu,
                          'doc_type': doc_type,
                          'meeting_id': meeting_id,
                          'meeting': meeting,
                          'meeting_duration': meeting_duration,
                          'meeting_end_time': meeting_end_time,
                          'completed_tasks_list': completed_tasks_list,
                          'incomplete_tasks_list': incomplete_tasks_list,
                          'meeting_form': meeting_form,
                          'next_meeting_form': next_meeting_form,
                          'item_formlist': item_formlist,
                          'task_formlist': task_formlist,
                          'decision_formlist': decision_formlist,
                          'decisions': decisions,
                          'tasks': tasks,
                          })
        responses.append(response)
    response = get_response(responses, request_type)

    return response


def minutes_distribute(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'minutes'
    participants = Participant.lists.active().filter(group=group)
    pages = create_pdf(request, group, meeting, doc_type)

    if request.method == "POST":
        if 'distribute_button' in request.POST:
            if request.POST['distribute_button']=='distribute':
                undraft_tasks_and_decisions(group, meeting)
                distribute_pdf(request, group, meeting, doc_type)
                archive_meeting(request, group, meeting_id=meeting_id)
                return HttpResponseRedirect(reverse('minutes-sent',
                                                    args=(meeting_id,)))

    menu = {'parent': 'meetings',
            'child': 'current_meetings',
            'tips': 'review_minutes'}
    return render(request, 'document_distribute.html', {
                  'menu': menu,
                  'doc_type': doc_type,
                  'meeting_id': meeting_id,
                  'pages': pages,
                  'participants': participants,
                  })


def minutes_print(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    pdf_contents = get_pdf_preview_contents(request, group, meeting, 'minutes')
    file_name = group.slug + '_minutes_' + meeting.meeting_no + '.pdf'

    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + file_name

    return response


def minutes_sent(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'minutes'
    meeting_no = meeting.meeting_no

    menu = {'parent': 'meetings'}
    return render(request, 'document_sent.html', {
                  'menu': menu,
                  'meeting_no': meeting_no,
                  'doc_type': doc_type,
                  })


def minutes_view(request, meeting_id):
    group = get_current_group(request)
    if group == None:
        return HttpResponseRedirect(reverse('index'))

    meeting = Meeting.objects.get(pk=int(meeting_id))
    if meeting.group != group:
        return HttpResponseRedirect(reverse('index'))

    doc_type = 'minutes'
    version = meeting.current_minutes_version
    base_file_name = get_base_file_name(request, group, meeting, 'minutes')
    pages = create_images_from_pdf(base_file_name, version=version)

    menu = {'parent': 'meetings'}
    return render(request, 'document_view.html', {
                  'menu': menu,
                  'doc_type': doc_type,
                  'meeting_id': meeting_id,
                  'pages': pages,
                  })
