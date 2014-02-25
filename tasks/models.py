from django.db import models
from django.contrib.auth.models import User

from docs.models import Item
from meetings.models import Meeting
from participants.models import Participant


class Task(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	meeting = models.ForeignKey(Meeting, null=True, blank=True)
	item = models.ForeignKey(Item, null=True, blank=True)
	participant = models.ForeignKey(Participant, null=True)
	description = models.CharField(max_length=200, blank=True)
	deadline = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=10, choices=(('Incomplete', 'Incomplete'), ('Complete', 'Complete')), blank=True)
	
	def __unicode__(self):
		return self.description
