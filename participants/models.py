from django.db import models
from utilities.models import TimeStampedModel

from accounts.models import Group


class ParticipantManager(models.Manager):

    def by_first_name(self):
        return self.get_queryset().all().order_by('first_name')
                
    def by_last_name(self):
        return self.get_queryset().all().order_by('last_name')

    def newest_first(self):
        return self.get_queryset().all().order_by('created').reverse()
        
        
class Participant(TimeStampedModel):
    
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Cancelled', 'Cancelled'),
        )
    
    group = models.ForeignKey(Group)
    
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    no_reminders = models.BooleanField(default=False) 
    notes = models.TextField(null=False, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=True)
    status = models.CharField(max_length=20, 
                              choices=STATUS_CHOICES,
                              default='Active',
                              blank=True)

    objects = models.Manager()
    lists = ParticipantManager()
    
    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])
