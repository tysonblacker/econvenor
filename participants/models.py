from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group


class Participant(TimeStampedModel):
    
    group = models.ForeignKey(Group)
    
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    no_reminders = models.BooleanField(default=False) 
    notes = models.TextField(null=False, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=True)
    status = models.CharField(max_length=20, null=False, blank=True)

    
    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])
