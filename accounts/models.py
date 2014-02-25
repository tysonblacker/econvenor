from django.db import models
from django.contrib.auth.models import User

		
class Account(models.Model):
	owner = models.ForeignKey(User, null=True, blank=True)
	date_altered = models.DateField(auto_now_add=True)
	group_name = models.CharField(max_length=200, blank=True)
	
	def __unicode__(self):
		return self.owner
