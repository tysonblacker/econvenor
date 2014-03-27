import datetime

from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from docs.models import Item
from meetings.models import Meeting
from participants.models import Participant


class TaskManager(models.Manager):

    def all_tasks(self):
        return self.get_queryset().all().order_by('deadline')
                
    def completed_tasks(self):
        return self.get_queryset().filter(status='Completed').\
            order_by('completion_date').reverse()

    def incomplete_tasks(self):
        return self.get_queryset().filter(status='Incomplete').\
            order_by('deadline')

    def overdue_tasks(self):
        return self.get_queryset().filter(
                status='Incomplete',
                deadline__lt=datetime.date.today())\
            .order_by('deadline')

    def pending_tasks(self):
        return self.get_queryset().filter(
                status='Incomplete',
                deadline__gte=datetime.date.today())\
            .order_by('deadline')
            
    def by_participant(self):
        return self.get_queryset().all().order_by('participant')
                    

class Task(TimeStampedModel):

    STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        )
   
    group = models.ForeignKey(Group)
    
    item = models.ForeignKey(Item, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    participant = models.ForeignKey(Participant,
                                    verbose_name='person responsible',
                                    null=True, blank=False)
    completion_date = models.DateField('date completed', null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=80, null=False, blank=True)
    notes = models.TextField('notes (optional)', max_length=300, null=False,
                             blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='Incomplete',
                              null=False,
                              blank=True)
    
    objects = models.Manager()
    lists = TaskManager()
    
    def __unicode__(self):
        return self.description
