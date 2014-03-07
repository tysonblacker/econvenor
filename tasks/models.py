from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from docs.models import Item
from meetings.models import Meeting
from participants.models import Participant


class Task(TimeStampedModel):

    group = models.ForeignKey(Group)
    
    item = models.ForeignKey(Item, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    participant = models.ForeignKey(Participant, null=True, blank=False)

    deadline = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=False, blank=True)
    status = models.CharField(max_length=10, choices=(
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
        ('Cancelled', 'Cancelled'),
        ),
        null=False, blank=True)

    def __unicode__(self):
        return self.description
