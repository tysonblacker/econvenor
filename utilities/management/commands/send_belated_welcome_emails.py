from string import replace

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError

from utilities.commonutils import set_path


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Initialises the user and group update logs.
        For use once only, on 11APR2014.
        """
        # Select users who registered before welcome emails were
        # automatically sent to new users
        users = User.objects.filter(id__gt=1)
        for user in users:
            group = user.usersettings.current_group
            send_belated_welcome_email(group=group, user=user)


def create_email_contents(template_file, name, signup_date, group, email):
    """
    Accepts a file containing an email template, recipient name,
    group name and recipient email address.
    Returns email content as a string.
    """
    f = open(template_file, 'r')
    template = f.read()
    f.close()

    contents = template.replace('{name}', name, 1)
    contents = contents.replace('{signup_date}', signup_date, 1)
    contents = contents.replace('{group}', group, 1)
    contents = contents.replace('{email}', email, 1)

    return contents


def send_belated_welcome_email(group, user):
    """
    Sends a welcome email when a user sets up an account.
    """
    recipient_email = user.email
    recipient_name = user.first_name
    recipient = [recipient_email]
    bcc = ['welcome@econvenor.org']
    group = group.name
    signup_date = user.date_joined.strftime("%B %d")
    if signup_date[-2] == '0':
        signup_date = replace(signup_date, '0', '')

    EMAIL_PATH = set_path('utilities/management/commands/templates/',
        '/home/econvenor/webapps/econvenor/econvenor/utilities/management/'
        'commands/templates/')

    text_template_file = EMAIL_PATH + 'welcome_email_belated.txt'
    html_template_file = EMAIL_PATH + 'welcome_email_belated.html'
    sender = 'eConvenor <mail@econvenor.org>'
    subject = 'A belated welcome to eConvenor!'
    text_content = create_email_contents(text_template_file, recipient_name,
                                         signup_date, group, recipient_email)
    html_content = create_email_contents(html_template_file, recipient_name,
                                         signup_date, group, recipient_email)
    msg = EmailMultiAlternatives(subject, text_content, sender, recipient, bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
