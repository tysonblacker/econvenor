from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date = models.DateField()
	location = models.TextField()
	description = models.CharField(max_length=100, choices=(('Ordinary meeting', 'Ordinary meeting'), ('Special meeting', 'Special meeting')), blank=True)
	agenda_locked = models.BooleanField(default=False)

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
	heading = models.CharField(max_length=100)
	time_limit = models.IntegerField(blank=True)
	explainer = models.ForeignKey(Participant, null=True, blank=True)
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
		
		
class Account(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date_altered = models.DateField(auto_now_add=True)
	group_name = models.CharField(max_length=200, blank=True)
	
	def __unicode__(self):
		return self.owner
		

class Bug(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date = models.DateField(auto_now_add=True)
	title = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=200, blank=True)
	trigger = models.TextField(blank=True)
	behaviour = models.TextField(blank=True)
	goal = models.TextField(blank=True)	
	status = models.CharField(max_length=10, choices=(('Open', 'Open'), ('Closed', 'Closed')), blank=True)
	priority = models.CharField(max_length=10, choices=(('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')), blank=True)
	comment = models.TextField(blank=True)	
		
	def __unicode__(self):
		return 'Bug ' + self.id + ': ' + self.title 


class Feature(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date = models.DateField(auto_now_add=True)
	title = models.CharField(max_length=100, blank=True)
	goal = models.TextField(blank=True)
	shortcoming = models.TextField(blank=True)
	suggestion = models.TextField(blank=True)	
	status = models.CharField(max_length=10, choices=(('Open', 'Open'), ('Closed', 'Closed')), blank=True)
	priority = models.CharField(max_length=10, choices=(('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')), blank=True)
	comment = models.TextField(blank=True)	
	
	def __unicode__(self):
		return 'Feature request ' + self.id + ': ' + self.title 

