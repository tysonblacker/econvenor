from django.db import models
from django.contrib.auth.models import User


class Decision(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	meeting = models.ForeignKey(Meeting)
	item = models.ForeignKey(Item)
	description = models.TextField()
	
	def __unicode__(self):
		return self.description
