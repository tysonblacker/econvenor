from django.core.validators import MaxLengthValidator
from django.db import models

from accounts.models import Group
from participants.auth import current_participant_token
from utilities.models import TimeStampedModel


class ParticipantManager(models.Manager):

    def by_first_name(self):
        return self.get_queryset().all().order_by('first_name')

    def by_last_name(self):
        return self.get_queryset().all().order_by('last_name')

    def newest_first(self):
        return self.get_queryset().all().order_by('created').reverse()

    def active(self):
        return self.get_queryset().filter(status='Active').\
            order_by('first_name')

    def inactive(self):
        return self.get_queryset().filter(status='Inactive').\
            order_by('first_name')

    def former(self):
        return self.get_queryset().filter(status='Former').\
            order_by('first_name')

    def receiving_reminders(self):
        return self.get_queryset().filter(status='Active', reminders=True).\
            order_by('first_name')

class Participant(TimeStampedModel):

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Former', 'Former'),
        )

    group = models.ForeignKey(Group)

    email = models.EmailField('email address', null=True, blank=True)
    first_name = models.CharField('given name', max_length=25, null=False,
                                  blank=True)
    last_name = models.CharField('family name (optional)', max_length=25,
                                 null=False, blank=True)
    reminders = models.BooleanField(default=True)
    notes = models.TextField('notes (optional)',
                             validators=[MaxLengthValidator(300)],
                             null=False, blank=True)
    phone = models.CharField('phone number (optional)', max_length=20,
                             null=False, blank=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Active',
                              blank=True)

    objects = models.Manager()
    lists = ParticipantManager()

    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])

    def current_token(self):
        """Generate today's token for this participant."""
        return current_participant_token(self.id)
