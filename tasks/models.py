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
                
    def complete_tasks(self):
        return self.get_queryset().filter(status='Complete').\
            order_by('deadline')

    def incomplete_tasks(self):
        return self.get_queryset().filter(status='Incomplete').\
            order_by('deadline')

    def overdue_tasks(self):
        return self.get_queryset().filter(
                status='Incomplete',
                deadline__lte=datetime.date.today())\
            .order_by('deadline')

    def by_participant(self):
        return self.get_queryset().all().order_by('participant')
                    

class Task(TimeStampedModel):

    STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
        ('Cancelled', 'Cancelled'),
        )
   
    group = models.ForeignKey(Group)
    
    item = models.ForeignKey(Item, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    participant = models.ForeignKey(Participant, null=True, blank=False)

    deadline = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=False, blank=True)
    notes = models.TextField(null=False, blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='Incomplete',
                              null=False,
                              blank=True)
    
    objects = models.Manager()
    lists = TaskManager()
    
    def __unicode__(self):
        return self.description
