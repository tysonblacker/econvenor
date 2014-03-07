from django.db import models
from django.contrib.auth.models import User

from utilities.models import TimeStampedModel


class Bug(TimeStampedModel):

    user = models.ForeignKey(User)

    behaviour = models.TextField(null=False, blank=True)
    comment = models.TextField(null=False, blank=True)	
    goal = models.TextField(null=False, blank=True)
    priority = models.CharField(
        max_length=30,
        choices=(
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High')
            ),
        null=False, blank=True
    )
    location = models.CharField(max_length=200, null=False,
                                blank=True)         
    status = models.CharField(
        max_length=30,
        choices=(
            ('Open', 'Open'),
            ('Closed', 'Closed')
            ),
        null=False, blank=True
    )  	
    title = models.CharField(max_length=100, null=False, blank=True)
    trigger = models.TextField(null=False, blank=True)
    
    def __unicode__(self):
        return 'Bug ' + self.id + ': ' + self.title


class Feature(TimeStampedModel):

    user = models.ForeignKey(User)

    comment = models.TextField(null=False, blank=True)	
    goal = models.TextField(null=False, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=(
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High')
            ),
        null=False, blank=True
    )
    shortcoming = models.TextField(null=False, blank=True)
    status = models.CharField(
        max_length=10,
            choices=(
                ('Open', 'Open'),
                ('Closed', 'Closed')
            ),
        null=False, blank=True
    )
    suggestion = models.TextField(null=False, blank=True)
    title = models.CharField(max_length=100, null=False, blank=True)

    def __unicode__(self):
        return 'Feature request ' + self.id + ': ' + self.title 
