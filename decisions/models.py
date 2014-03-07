from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from docs.models import Item
from meetings.models import Meeting


class Decision(TimeStampedModel):

    group = models.ForeignKey(Group)

    item = models.ForeignKey(Item)
    meeting = models.ForeignKey(Meeting)
    
    description = models.TextField(null=False, blank=False)
    
    def __unicode__(self):
        return self.description
