from django.db import models
from utilities.models import TimeStampedModel

from django.contrib.auth.models import User

from accounts.models import Account, Group
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


class AccountUpdate(TimeStampedModel):
    """
    The is only used for recording updates
    to a user's account settings.
    """
    
    user = models.ForeignKey(User)

    account = models.ForeignKey(Account)

    field = models.CharField(max_length=100, null=False, blank=True)
    old_value = models.TextField(null=False, blank=True)
    new_value = models.TextField(null=False, blank=True)
