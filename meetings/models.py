from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from participants.models import Participant


class MeetingManager(models.Manager):

    def all_meetings(self):
        return self.get_queryset().all().order_by('meeting_no')


class Meeting(TimeStampedModel):

    MEETING_TYPE_CHOICES = (
        ('Ordinary meeting', 'Ordinary meeting'),
        ('Working group meeting', 'Working group meeting'),
        ('Annual General Meeting', 'Annual General Meeting'),
        ('Special Meeting', 'Special Meeting'),
        )
    MEETING_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
        ('Cancelled', 'Cancelled'),
        )
            
    group = models.ForeignKey(Group)

    agenda_pdf = models.FileField(upload_to='meetingdocs')
    apologies = models.TextField(null=False, blank=True)
    attendance = models.TextField(null=False, blank=True)            
    meeting_no = models.CharField(max_length=30, null=False, blank=True)
    meeting_type = models.CharField(max_length=30, 
                                    choices=MEETING_TYPE_CHOICES,
                                    null=False,
                                    blank=True)
    meeting_status = models.CharField(max_length=30, 
                                      choices=MEETING_STATUS_CHOICES,
                                      null=False, blank=True)
    minutes_pdf = models.FileField(upload_to='meetingdocs')    
    reminder_sent = models.DateTimeField(null=True, blank=True)
    
    objects = models.Manager()
    lists = MeetingManager()
   
    def __unicode__(self):
        return ' on '.join([self.description, str(self.date)])


class MeetingDetails(TimeStampedModel):
        
    group = models.ForeignKey(Group)
        
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    
    date = models.DateField(null=True, blank=True)
    details_type = models.CharField(max_length=30, null=False, blank=True)
    end_time = models.TimeField(null=True, blank=True)    
    facilitator = models.ForeignKey(Participant, null=True, blank=True,
                                    related_name='facilitator_related')
    instructions = models.TextField(null=False, blank=True)
    location = models.TextField(null=False, blank=True)
    minute_taker = models.ForeignKey(Participant, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)  


class DistributionRecord(TimeStampedModel):

    group = models.ForeignKey(Group)
        
    meeting = models.ForeignKey(Meeting, null=True, blank=True)

    covering_message = models.TextField(null=False, blank=True)
    date_and_time = models.DateTimeField()
    distribution_list = models.TextField(null=False, blank=True)
