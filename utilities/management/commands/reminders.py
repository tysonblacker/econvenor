from datetime import date,timedelta

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from accounts.models import Group
from tasks.models import Task
from participants.auth import EXPIRY_DAYS
from participants.models import Participant


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Generates a list of due and overdue tasks for each participant, and
        also a summary of due and overdue tasks for the group convenor/s.
        """
        groups = Group.lists.active_groups()
        yesterday = date.today() - timedelta(1)
        for group in groups:
            participants = Participant.lists.receiving_reminders().\
                           filter(group=group)
            all_due_tasks = []
            all_overdue_tasks = []
            for participant in participants:
                due_tasks = []
                overdue_tasks = []
                send_reminder = False
                # Set the number of days at which due tasks trigger an email
                reminder_interval = 3
                # Create a list of all of this participant's incomplete tasks
                try:
                    tasks = Task.lists.incomplete_tasks().\
                            filter(group=group, participant=participant)
                except tasks.DoesNotExist:
                    pass
                # Create lists of tasks to remind this participant about
                for task in tasks:
                    time_to_deadline = task.deadline - date.today()
                    if (time_to_deadline.days <= reminder_interval) and \
                       (time_to_deadline.days >= 0):
                        due_tasks.append(task)
                        if time_to_deadline.days == reminder_interval:
                            send_reminder = True
                    if task.deadline <= yesterday:
                        overdue_tasks.append(task)
                        if task.deadline == yesterday:
                            send_reminder = True
                if send_reminder:
                    # Add tasks to lists for the group convenor
                    all_due_tasks.extend(due_tasks)
                    all_overdue_tasks.extend(overdue_tasks)
                    # Send the email to the participant
                    send_reminder_email(group, participant, reminder_interval,
                                        due_tasks, overdue_tasks)

            if all_due_tasks or all_overdue_tasks:
                # Once all reminders have been sent, send a summary email to
                # the convenor
                send_summary_email(group, reminder_interval, all_due_tasks,
                                   all_overdue_tasks)


def send_reminder_email(group, participant, reminder_interval, due_tasks,
                        overdue_tasks):
    """
    Emails a reminder about due and overdue tasks to the participants
    they are assigned to.
    """
    # Set up email fields
    recipient = [participant.email]
    recipient_name = participant.first_name
    group_name = group.name
    convenor_name = group.users.get().first_name
    convenor_email = group.users.get().email
    sender = 'eConvenor <noreply@econvenor.org>'
    subject = group_name + ': A reminder about your tasks'
    bcc = ['qa@econvenor.org']
    # Generate the email body in html and plain text
    context_dictionary = {'convenor_email': convenor_email,
                          'convenor_name': convenor_name,
                          'due_tasks': due_tasks,
                          'group_name': group_name,
                          'overdue_tasks': overdue_tasks,
                          'recipient_name': recipient_name,
                          'reminder_interval': reminder_interval,
                          'participant': participant,
                          'expiry_days': EXPIRY_DAYS,
                          'participant_task_url': 'https://econvenor.org%s' % (
                              reverse(
                                'my-tasks-auth',
                                args=(
                                    participant.id,
                                    participant.current_token,
                                ),
                              ),
                          ),
                          }
    text_content = create_email_contents('email_reminder_participant.txt',
                                         context_dictionary)
    html_content = create_email_contents('email_reminder_participant.html',
                                         context_dictionary)
    # Send the email
    msg = EmailMultiAlternatives(subject, text_content, sender, recipient, bcc,
                                 headers = {'Reply-To': convenor_email})
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_summary_email(group, reminder_interval, all_due_tasks,
                       all_overdue_tasks):
    """
    Emails a summary of the day's email notifications to the convenor.
    """
    # Set up email fields
    convenor_name = group.users.get().first_name
    convenor_email = group.users.get().email
    group_name = group.name
    recipient = [convenor_email]
    sender = 'eConvenor <noreply@econvenor.org>'
    subject = group_name + ': Summary of today\'s task reminders'
    bcc = ['qa@econvenor.org']
    # Sort the task lists by deadline
    all_overdue_tasks.sort(key=lambda x: str(x.deadline))
    all_due_tasks.sort(key=lambda x: str(x.deadline))
    # Generate the email body in html and plain text
    context_dictionary = {'all_due_tasks': all_due_tasks,
                          'all_overdue_tasks': all_overdue_tasks,
                          'convenor_name': convenor_name,
                          'group_name': group_name,
                          'reminder_interval': reminder_interval,
                          }
    text_content = create_email_contents('email_reminder_summary.txt',
                                         context_dictionary)
    html_content = create_email_contents('email_reminder_summary.html',
                                         context_dictionary)
    # Send the email
    msg = EmailMultiAlternatives(subject, text_content, sender, recipient, bcc)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def create_email_contents(template_file, context_dictionary):
    """
    Accepts an email template file name and a dictionary of content variables.
    Returns email content as a string.
    """
    contents = render_to_string(template_file, context_dictionary)
    return contents
