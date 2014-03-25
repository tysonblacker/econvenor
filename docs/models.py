from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group
from meetings.models import Meeting
from participants.models import Participant


class ItemManager(models.Manager):

    def all_items(self):
        return self.get_queryset().all().order_by('item_no')


class Item(TimeStampedModel):

    TIME_LIMIT_CHOICES = (
        (2,2), (5,5), (10,10), (15,15), (20,20), (25,25), (30,30), (35,35),
        (40,40), (45,45), (50,50), (55,55), (60,60), (75,75), (90,90),
        (120,120), (150,150), (180,180), (210,210), (240,240), (300,300),
        )
        
    group = models.ForeignKey(Group)

    explainer = models.ForeignKey(Participant, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)

    added_in_meeting = models.BooleanField(default=False)
    background = models.TextField('background information', null=False,
                                  blank=True)
    carry_over = models.BooleanField(default=False)
    item_no = models.IntegerField(null=True, blank=True)
    minute_notes = models.TextField('minutes', null=False, blank=True)
    time_limit = models.IntegerField('time limit (mins)',
                                     choices=TIME_LIMIT_CHOICES,
                                     null=True, blank=True)
    title = models.CharField('item title', max_length=100, null=False,
                             blank=True)

    objects = models.Manager()
    lists = ItemManager()

    def __unicode__(self):
        return str(self.item_no) + ': ' + self.title


class Template(TimeStampedModel):

    group = models.ForeignKey(Group)

    name = models.CharField(max_length=30, null=False, blank=True)
    data = models.TextField(null=False, blank=True)

