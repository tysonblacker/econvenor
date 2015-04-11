from django.db import models
from utilities.models import TimeStampedModel
import uuid
import os

from django.contrib.auth.models import User


def get_file_path(instance, filename):
    """
    This is was used to create unique names for uploaded files.
    Currently not used but left incase it is needed in the future. 
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('logos', filename)

class GroupManager(models.Manager):

    def all_groups(self):
        return self.get_queryset().all().order_by('name')

    def active_groups(self):
        return self.get_queryset().filter(account_status='Active').\
            order_by('name')

    def newest_groups(self):
        return self.get_queryset().filter(account_status='Active').\
            order_by('created').reverse()[:5]

class Group(TimeStampedModel):

    ACCOUNT_TYPE_CHOICES = (
        ('Free', 'Free'),
        ('Paid', 'Paid'),
        ('Trial', 'Trial'),
        )
    ACCOUNT_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Abandoned', 'Abandoned'),
        ('Suspended', 'Suspended'),
        )

    users = models.ManyToManyField(User)

    aim = models.CharField('group aim', max_length=100, null=False,
                           blank=True)
    country = models.CharField(max_length=40, null=False, blank=True)
    focus = models.CharField('main area of focus', max_length=40, null=False,
                             blank=True)
    logo = models.FileField(upload_to='logos')
    name = models.CharField(max_length=100, null=False, blank=True)
    slug = models.SlugField(null=False, blank=True)
    account_status = models.CharField(max_length=20,
                                      choices=ACCOUNT_STATUS_CHOICES,
                                      default='Active',
                                      null=False, blank=True)
    account_type = models.CharField(max_length=20,
                                    choices=ACCOUNT_TYPE_CHOICES,
                                    default='Free', null=False, blank=True)

    objects = models.Manager()
    lists = GroupManager()

    def __unicode__(self):
        return self.name


class UserSettings(TimeStampedModel):

    user = models.OneToOneField(User, primary_key=True)
    current_group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.current_group.value

