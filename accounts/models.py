from django.db import models
from utilities.models import TimeStampedModel

from django.contrib.auth.models import User


class Account(TimeStampedModel):

    user = models.ForeignKey(User, null=True, blank=True)

    email = models.EmailField()
    first_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(max_length=50, null=False, blank=True)
    username = models.CharField(max_length=30, null=False, blank=True)
            
    def __unicode__(self):
        return self.user


class Group(TimeStampedModel):

    account = models.ForeignKey(Account)
    
    description = models.CharField(max_length=200, null=False, blank=True)
    logo = models.FileField(upload_to='logos')
    name = models.CharField(max_length=100, null=False, blank=True)
    status = models.CharField(max_length=20, null=False, blank=True)
    
    def __unicode__(self):
        return self.name
