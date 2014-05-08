from django.core.management.base import BaseCommand, CommandError

from meetings.models import Meeting


class Command(BaseCommand): 

    def handle(self, *args, **options):
        """
        Sets the status of meetings which are archived to 'Complete'. The
        status of archived meetings was incorrectly being left as 'Scheduled'
        due to a bug.
        For use once only, on 08MAY2014.
        """
        archived_meetings = Meeting.lists.archived_meetings()
        for meeting in archived_meetings:
            meeting.meeting_status = 'Completed'
            meeting.save()
