from django.db import models
from django.contrib.auth.models import User
		

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
