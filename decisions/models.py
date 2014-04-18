from django.core.validators import MaxLengthValidator
from django.db import models

from accounts.models import Group
from docs.models import Item
from meetings.models import Meeting
from utilities.models import TimeStampedModel


class DecisionManager(models.Manager):

    def all_decisions(self):
        return self.get_queryset().filter(status='Distributed').\
            order_by('modified').reverse()

    def ordered_decisions(self):
        return self.get_queryset().all().order_by('decision_no')

class Decision(TimeStampedModel):

    STATUS_CHOICES = (
        ('Distributed', 'Distributed'),
        ('Draft', 'Draft'),
        )
        
    group = models.ForeignKey(Group)

    item = models.ForeignKey(Item)
    meeting = models.ForeignKey(Meeting)
    
    decision_no = models.IntegerField(null=True, blank=True)
    description = models.TextField(validators=[MaxLengthValidator(300)],
                                   null=False, blank=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Draft',
                              null=False,
                              blank=True)
    
    objects = models.Manager()
    lists = DecisionManager()
        
    def __unicode__(self):
        return self.description
