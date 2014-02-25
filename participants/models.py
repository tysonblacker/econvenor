from django.db import models
from django.contrib.auth.models import User


class Participant(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100, blank=True)
	email_address = models.EmailField()
	phone_number = models.CharField(max_length=20)
#	notes = models.TextField()
	
	def __unicode__(self):
		return ' '.join([self.first_name, self.last_name])
