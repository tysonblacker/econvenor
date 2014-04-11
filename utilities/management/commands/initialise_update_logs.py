from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from accounts.models import Group
from common.utils import snapshot_group_details, \
                         snapshot_user_details

class Command(BaseCommand): 

    def handle(self, *args, **options):
        """
        Initialises the user and group update logs.
        For use once only, on 11APR2014.
        """
        users = User.objects.all()
        for user in users:
            snapshot_user_details(user, password='set')

        groups = Group.objects.all()
        for group in groups:
            snapshot_group_details(group)
