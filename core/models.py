from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date = models.DateTimeField()
	location = models.TextField()
	description = models.CharField(max_length=100, choices=(('Ordinary meeting', 'Ordinary meeting'), ('Special meeting', 'Special meeting')), blank=True)
	agenda_locked = models.BooleanField()

	def __unicode__(self):
		return ' on '.join([self.description, str(self.date)])


class Participant(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100, blank=True)
	email_address = models.EmailField()
	phone_number = models.CharField(max_length=20)
#	notes = models.TextField()
	
	def __unicode__(self):
		return ' '.join([self.first_name, self.last_name])
    	
    	
class Item(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	meeting = models.ForeignKey(Meeting)
#	participant = models.ForeignKey(Participant)
	heading = models.CharField(max_length=100)
	background = models.TextField(blank=True)
	variety = models.CharField(max_length=20, blank=True) # 'preliminary', 'main', etc
	minute_notes = models.TextField(blank=True)

	def __unicode__(self):
		return self.heading


class Decision(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	meeting = models.ForeignKey(Meeting)
	item = models.ForeignKey(Item)
	description = models.TextField()
	
	def __unicode__(self):
		return self.description


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
