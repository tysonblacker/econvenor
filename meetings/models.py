from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from participants.models import Participant


class Meeting(TimeStampedModel):

    group = models.ForeignKey(Group)

    agenda_pdf = models.FileField(upload_to='meetingdocs')
    apologies = models.TextField(null=False, blank=True)
    attendance = models.TextField(null=False, blank=True)            
    meeting_no = models.CharField(max_length=30, null=False, blank=True)
    meeting_type = models.CharField(
        max_length=100, 
            choices=(
                ('Ordinary meeting', 'Ordinary meeting'),
                ('Working group meeting', 'Working group meeting'),
                ('Annual General Meeting', 'Annual General Meeting'),
            ),
        null=False, blank=True)
    meeting_status = models.CharField(
        max_length=30, 
            choices=(
                ('Pending', 'Pending'),
                ('Complete', 'Complete'),
                ('Cancelled', 'Cancelled'),
            ),
        null=False, blank=True)
    minutes_pdf = models.FileField(upload_to='meetingdocs')    
    reminder_sent = models.DateTimeField()
   
    def __unicode__(self):
        return ' on '.join([self.description, str(self.date)])


class MeetingDetails(TimeStampedModel):

    group = models.ForeignKey(Group)
        
    meeting = models.ForeignKey(Meeting)
    
    date = models.DateField(null=True, blank=True)
    details_type = models.CharField(max_length=30, null=False, blank=True)
    end_time = models.TimeField(null=True, blank=True)    
    facilitator = models.ForeignKey(Participant, null=True, blank=True,
                                    related_name='facilitator_related')
    instructions = models.TextField(null=False, blank=True)
    location = models.TextField(null=False, blank=True)
    minute_taker = models.ForeignKey(Participant, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)  


class SendRecord(TimeStampedModel):

    group = models.ForeignKey(Group)
        
    meeting = models.ForeignKey(Meeting)

    covering_message = models.TextField(null=False, blank=True)
    date_and_time = models.DateTimeField()
    distribution_list = models.TextField(null=False, blank=True)
