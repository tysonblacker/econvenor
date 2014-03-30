from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from docs.models import Item
from meetings.models import Meeting


class TaskManager(models.Manager):
    def all_decisions(self):
        return self.get_queryset().filter(status='Distributed').\
            order_by('modified').reverse()


class Decision(TimeStampedModel):

    STATUS_CHOICES = (
        ('Distributed', 'Distributed'),
        ('Draft', 'Draft'),
        )
        
    group = models.ForeignKey(Group)

    item = models.ForeignKey(Item)
    meeting = models.ForeignKey(Meeting)
    
    decision_no = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=300, null=False, blank=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Draft',
                              null=False,
                              blank=True)
    
    objects = models.Manager()
    lists = TaskManager()
        
    def __unicode__(self):
        return self.description
