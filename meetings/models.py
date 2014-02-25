from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date = models.DateField()
	start_time = models.TimeField(null=True, blank=True)
	location = models.TextField()
	notes = models.TextField(blank=True) 
	description = models.CharField(max_length=100, choices=(('Ordinary meeting', 'Ordinary meeting'), ('Special meeting', 'Special meeting')), blank=True)
	agenda_locked = models.BooleanField(default=False)

	def __unicode__(self):
		return ' on '.join([self.description, str(self.date)])
