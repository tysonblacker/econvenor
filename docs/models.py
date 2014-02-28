from django.contrib.auth.models import User
from django.db import models

from meetings.models import Meeting
from participants.models import Participant


class Item(models.Model):

    explainer = models.ForeignKey(Participant, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    meeting = models.ForeignKey(Meeting)

    background = models.TextField(blank=True)
    heading = models.CharField(max_length=100)
    item_no = models.IntegerField(blank=True)
    minute_notes = models.TextField(blank=True)
    time_limit = models.IntegerField(null=True, blank=True)


    def __unicode__(self):
        
        return ') '.join([str(self.item_no), self.heading])
