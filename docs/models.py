from django.db import models
from django.contrib.auth.models import User
    	
    	
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
