from django.core.validators import MaxLengthValidator
from django.db import models

from accounts.models import Group
from meetings.models import Meeting
from participants.models import Participant
from utilities.models import TimeStampedModel


class ItemManager(models.Manager):

    def all_items(self):
        return self.get_queryset().all().order_by('item_no')


class Item(TimeStampedModel):

    TIME_LIMIT_CHOICES = (
        (2,'2 mins'), (5,'5 mins'), (10,'10 mins'), (15,'15 mins'),
        (20,'20 mins'), (25,'25 mins'), (30,'30 mins'), (35,'35 mins'),
        (40,'40 mins'), (45,'45 mins'), (50,'50 mins'), (55,'55 mins'),
        (60,'60 mins'), (90,'90 mins'), (120,'120 mins'), (150,'150 mins'),
        (180,'180 mins'), (240,'240 mins'), (300,'300 mins'), (360,'360 mins'),
        )

    group = models.ForeignKey(Group)

    explainer = models.ForeignKey(Participant, null=True, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)

    added_in_meeting = models.BooleanField(default=False)
    background = models.TextField(validators=[MaxLengthValidator(1000)],
                                  null=False, blank=True)
    carry_over = models.BooleanField(default=False)
    item_no = models.IntegerField(null=True, blank=True)
    minute_notes = models.TextField(validators=[MaxLengthValidator(2000)],
                                    null=False, blank=True)
    time_limit = models.IntegerField(choices=TIME_LIMIT_CHOICES,
                                     null=True, blank=True)
    title = models.CharField(max_length=80, null=False, blank=True)

    objects = models.Manager()
    lists = ItemManager()

    def __unicode__(self):
        return str(self.item_no) + ': ' + self.title


class Template(TimeStampedModel):

    group = models.ForeignKey(Group)

    name = models.CharField(max_length=30, null=False, blank=True)
    data = models.TextField(null=False, blank=True)

