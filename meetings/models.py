from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from participants.models import Participant


class MeetingManager(models.Manager):

    def all_meetings(self):
        return self.get_queryset().all().order_by('meeting_no')


class Meeting(TimeStampedModel):

    MEETING_TYPE_CHOICES = (
        ('Ordinary Meeting', 'Ordinary Meeting'),
        ('Working Group Meeting', 'Working Group Meeting'),
        ('Annual General Meeting', 'Annual General Meeting'),
        ('Special Meeting', 'Special Meeting'),
        )
    MEETING_STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Complete', 'Complete'),
        ('Cancelled', 'Cancelled'),
        )
            
    group = models.ForeignKey(Group)

    agenda_pdf = models.FileField(upload_to='meeting_docs')
    apologies = models.TextField(null=False, blank=True)
    attendance = models.TextField(null=False, blank=True)            
    meeting_no = models.CharField(max_length=20, null=False, blank=True)
    meeting_type = models.CharField(max_length=30, 
                                    choices=MEETING_TYPE_CHOICES,
                                    default='Ordinary Meeting',
                                    null=False,
                                    blank=True)
    meeting_status = models.CharField(max_length=30, 
                                      choices=MEETING_STATUS_CHOICES,
                                      default='Scheduled',
                                      null=False, blank=True)
    minutes_pdf = models.FileField(upload_to='meeting_docs')    
    reminder_sent = models.DateTimeField(null=True, blank=True)
    date_scheduled = models.DateField(null=True, blank=True)
    date_actual = models.DateField(null=True, blank=True)
    end_time_actual = models.TimeField(null=True, blank=True)  
    facilitator_scheduled = models.ForeignKey(Participant,
                                              related_name='facilitator_sch',
                                              null=True, blank=True)
    facilitator_actual = models.ForeignKey(Participant,
                                           related_name='facilitator_act',
                                           null=True, blank=True)
    instructions_scheduled = models.TextField(max_length=200, null=False,
                                              blank=True)
    instructions_actual = models.TextField(max_length=200, null=False,
                                           blank=True)
    location_scheduled = models.TextField(max_length=200, null=False,
                                          blank=True)
    location_actual = models.TextField(max_length=200, null=False, blank=True)
    minute_taker_scheduled = models.ForeignKey(Participant,
                                               related_name='minutetaker_sch',
                                               null=True, blank=True)
    minute_taker_actual = models.ForeignKey(Participant,
                                            related_name='minutetaker_act',
                                            null=True, blank=True)
    start_time_scheduled = models.TimeField(null=True, blank=True)
    start_time_actual = models.TimeField(null=True, blank=True)
    next_meeting_date = models.DateField(null=True, blank=True)
    next_meeting_facilitator = models.ForeignKey(Participant,
                                              related_name='facilitator_next',
                                              null=True, blank=True)
    next_meeting_instructions = models.TextField(max_length=200, null=False,
                                                 blank=True)
    next_meeting_location = models.TextField(max_length=200, null=False,
                                             blank=True)
    next_meeting_minute_taker = models.ForeignKey(Participant, null=True,
                                               related_name='minutetaker_next',
                                               blank=True)
    next_meeting_start_time = models.TimeField(null=True, blank=True)
    
    objects = models.Manager()
    lists = MeetingManager()
   
    def __unicode__(self):
        return ' on '.join([self.meeting_type, str(self.date_scheduled)])


class DistributionRecord(TimeStampedModel):

    group = models.ForeignKey(Group)
        
    meeting = models.ForeignKey(Meeting, null=True, blank=True)

    covering_message = models.TextField(null=False, blank=True)
    date_and_time = models.DateTimeField()
    distribution_list = models.TextField(null=False, blank=True)
    
    def __unicode__(self):
        return 'Distibuted on ' + date_and_time
