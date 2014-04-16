import datetime

from django.core.validators import MaxLengthValidator
from django.db import models

from accounts.models import Group
from participants.models import Participant
from utilities.models import TimeStampedModel


class MeetingManager(models.Manager):

    def all_meetings(self):
        return self.get_queryset().all().order_by('meeting_no')

    def current_meetings(self):
        return self.get_queryset().exclude(meeting_archived=True).\
            order_by('date_scheduled')

    def archived_meetings(self):
        return self.get_queryset().filter(meeting_archived=True).\
            order_by('date_actual').reverse()

    def past_meetings(self):
        return self.get_queryset().\
            filter(date_scheduled__lt=datetime.date.today()).\
            order_by('date_scheduled')

    def future_meetings(self):
        return self.get_queryset().\
            filter(date_scheduled__gte=datetime.date.today()).\
            order_by('date_scheduled')
                        
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
    apologies = models.TextField('apologies (optional)',
                                 validators=[MaxLengthValidator(200)],
                                 null=False, blank=True)
    attendance = models.TextField(validators=[MaxLengthValidator(200)],
                                  null=False, blank=True)            
    meeting_no = models.CharField(max_length=30, null=False, blank=True)
    meeting_type = models.CharField('type of meeting', max_length=30, 
                                    choices=MEETING_TYPE_CHOICES,
                                    default='Ordinary Meeting',
                                    null=False,
                                    blank=True)
    meeting_status = models.CharField('meeting status', max_length=30, 
                                      choices=MEETING_STATUS_CHOICES,
                                      default='Scheduled',
                                      null=False, blank=True)
    minutes_pdf = models.FileField(upload_to='meeting_docs')    
    reminder_sent = models.DateTimeField(null=True, blank=True)
    date_scheduled = models.DateField('date', null=True,
                                      blank=True)
    date_actual = models.DateField('date', null=True, blank=True)
    end_time_actual = models.TimeField('meeting end time', null=True,
                                       blank=True)  
    facilitator_scheduled = models.ForeignKey(
                            Participant, 
                            verbose_name='facilitator / chair (optional)',
                            related_name='facilitator_sch',
                            null=True, blank=True)
    facilitator_actual = models.ForeignKey(Participant,
                                           verbose_name='facilitator / chair',
                                           related_name='facilitator_act',
                                           null=True, blank=True)
    instructions_scheduled = models.TextField(
                             'instructions / notes (optional)',
                             validators=[MaxLengthValidator(200)],
                             null=False, blank=True)
    instructions_actual = models.TextField(
                          'notes (optional)',
                          validators=[MaxLengthValidator(200)],
                          null=False, blank=True)
    location_scheduled = models.TextField(
                         'location',
                         validators=[MaxLengthValidator(200)],
                         null=False, blank=True)
    location_actual = models.TextField(
                      'location', 
                      validators=[MaxLengthValidator(200)],
                      null=False, blank=True)
    minute_taker_scheduled = models.ForeignKey(
                             Participant,
                             verbose_name='minute taker (optional)',
                             related_name='minutetaker_sch',
                             null=True, blank=True)
    minute_taker_actual = models.ForeignKey(Participant,
                                            verbose_name='minute taker',    
                                            related_name='minutetaker_act',
                                            null=True, blank=True)
    start_time_scheduled = models.TimeField('start time', null=True,
                                            blank=True)
    start_time_actual = models.TimeField('start time', null=True, blank=True)
    next_meeting_date = models.DateField('date', null=True, blank=True)
    next_meeting_facilitator = models.ForeignKey(Participant,
                               verbose_name='facilitator / chair',
                               related_name='facilitator_next',
                               null=True, blank=True)
    next_meeting_instructions = models.TextField(
                                'instructions / notes',
                                validators=[MaxLengthValidator(200)],
                                null=False, blank=True)
    next_meeting_location = models.TextField(
                            'location',
                            validators=[MaxLengthValidator(200)],
                            null=False, blank=True)
    next_meeting_minute_taker = models.ForeignKey(Participant, null=True,
                                verbose_name='minute taker',
                                related_name='minutetaker_next', blank=True)
    next_meeting_start_time = models.TimeField('start time', null=True,
                                               blank=True)
    current_agenda_version = models.IntegerField(null=True, blank=True)
    current_minutes_version = models.IntegerField(null=True, blank=True)
    meeting_archived = models.BooleanField(default=False)
    
    objects = models.Manager()
    lists = MeetingManager()
   
    def __unicode__(self):
        return ' on '.join([self.meeting_type, str(self.date_scheduled)])


class DistributionRecord(TimeStampedModel):

    group = models.ForeignKey(Group)
        
    meeting = models.ForeignKey(Meeting, null=True, blank=True)

    covering_message = models.TextField(null=False, blank=True)
    distribution_list = models.TextField(null=False, blank=True)
    doc_type = models.CharField(max_length=30, null=False, blank=True)
    
    def __unicode__(self):
        return 'Distibuted the ' + doc_type + ' on ' + str(modified)
