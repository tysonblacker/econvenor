from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from meetings.models import Meeting
from participants.models import Participant


class Item(TimeStampedModel):

    group = models.ForeignKey(Group)

    explainer = models.ForeignKey(Participant, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)

    background = models.TextField(null=False, blank=True)
    carry_over = models.BooleanField(default=False)
    item_no = models.IntegerField(null=True, blank=True)
    minute_notes = models.TextField(null=False, blank=True)
    time_limit = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=True)

    def __unicode__(self):
        return str(self.item_no) + ': ' + self.title

#    def save(self, group, *args, **kwargs):
#        self.group = group
#        super(Item, self).save(*args, **kwargs)


class Template(TimeStampedModel):

    group = models.ForeignKey(Group)

    name = models.CharField(max_length=30, null=False, blank=True)
    data = models.TextField(null=False, blank=True)

