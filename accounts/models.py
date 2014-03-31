from django.db import models
from utilities.models import TimeStampedModel

from django.contrib.auth.models import User


class Group(TimeStampedModel):

    users = models.ManyToManyField(User)
    
    aim = models.CharField('group aim', max_length=200, null=False,
                           blank=True)
    country = models.CharField(max_length=40, null=False, blank=True)
    focus = models.CharField('main area of focus e.g. refugee rights, \
                             climate change', max_length=40, null=False,
                             blank=True)
    logo = models.FileField(upload_to='logos')
    name = models.CharField(max_length=100, null=False, blank=True)
    slug = models.SlugField(null=False, blank=True)
    status = models.CharField(max_length=20, null=False, blank=True)
    
    def __unicode__(self):
        return self.name
        

class UserSettings(TimeStampedModel):

    user = models.OneToOneField(User, primary_key=True)
    current_group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.current_group.value

