from django.db import models
from utilities.models import TimeStampedModel

from django.contrib.auth.models import User

from accounts.models import Group
from participants.models import Participant
from tasks.models import Task


class Update(TimeStampedModel):
    """
    This is used for recording updates everywhere
    but in a user's account settings.
    """
        
    user = models.ForeignKey(User)

    group = models.ForeignKey(Group)
    participant = models.ForeignKey(Participant)
    task = models.ForeignKey(Task)

    field = models.CharField(max_length=100, null=False, blank=True)
    old_value = models.TextField(null=False, blank=True)
    new_value = models.TextField(null=False, blank=True)


class UserUpdate(TimeStampedModel):
    """
    Records changes to a user's details.
    """
    
    user = models.ForeignKey(User)

    username = models.CharField(max_length=30, null=False, blank=True)
    first_name = models.CharField(max_length=30,null=False, blank=True)
    last_name = models.CharField(max_length=30, null=False, blank=True)
    email = models.EmailField(null=False, blank=True)
    password = models.CharField(max_length=20, null=False, blank=True)

class GroupUpdate(TimeStampedModel):
    """
    Records changes to a group's details.
    """
    
    group = models.ForeignKey(Group)
    
    aim = models.CharField(max_length=100, null=False, blank=True)
    country = models.CharField(max_length=40,null=False, blank=True)
    focus = models.CharField(max_length=40, null=False, blank=True)
    logo = models.FileField(upload_to='logos')
    name = models.CharField(max_length=100, null=False, blank=True)
    slug = models.SlugField(null=False, blank=True)
    account_status = models.CharField(max_length=20, null=False, blank=True)
    account_type = models.CharField(max_length=20, null=False, blank=True)

