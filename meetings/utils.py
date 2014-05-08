from meetings.models import Meeting, DistributionRecord


def find_or_create_distribution_record(group, meeting, doc_type):
    """
    Finds the distribution record for a document, or creates a blank
    one if none exists. Returns the distribution record.
    """
    try:
        record = DistributionRecord.objects.get(group=group, meeting=meeting, 
                                                doc_type=doc_type)
    except DistributionRecord.DoesNotExist:
        record = DistributionRecord(group=group,
                                    meeting=meeting,
                                    doc_type=doc_type,
                                    )
        record.save(group)
    
    return record


def archive_meeting(request, group, **kwargs):
    """
    Archives a meeting and sets its status to 'Completed'.
    """
    if kwargs:
        meeting_id = kwargs['meeting_id']
    else:
        meeting_id = request.POST['button'][8:]
    meeting = Meeting.objects.get(group=group, pk=int(meeting_id))
    meeting.meeting_archived = True
    meeting.meeting_status = 'Completed'
    meeting.save()


def delete_meeting(request, group):
    """
    Deletes a meeting.
    """
    meeting_id = request.POST['button'][7:]
    meeting = Meeting.objects.get(group=group, pk=int(meeting_id))
    meeting.delete()        


def unarchive_meeting(request, group):
    """
    Unarchives a meeting. Leaves its status as 'Completed'.
    """
    meeting_id = request.POST['button'][10:]
    meeting = Meeting.objects.get(group=group, pk=int(meeting_id))
    meeting.meeting_archived = False
    meeting.save()

