from datetime import date, timedelta

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError

from accounts.models import Group
from tasks.models import Task
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
            all_new_overdue_tasks = []
            all_old_overdue_tasks = []
            for participant in participants:
                due_tasks = []
                new_overdue_tasks = []
                old_overdue_tasks = []
                reminder_interval = 3 # Tasks due in 3 days trigger an email
                clear_due_tasks = True
                try:
                    tasks = Task.lists.incomplete_tasks().\
                            filter(group=group, participant=participant)
                except tasks.DoesNotExist:
                    pass
                # Create lists of tasks for this participant
                for task in tasks:
                    time_to_deadline = task.deadline - date.today()
                    if (time_to_deadline.days <= reminder_interval) and \
                       (time_to_deadline.days >= 0):
                        due_tasks.append(task)
                        if time_to_deadline.days == reminder_interval:
                            clear_due_tasks = False
                    if task.deadline == yesterday:
                        new_overdue_tasks.append(task)
                        clear_due_tasks = False
                    if task.deadline < yesterday:
                        old_overdue_tasks.append(task)
                # Only append due tasks if at least one is due in 3 days or
                # there is a new overdue task
                if clear_due_tasks:
                    due_tasks = []                    
                if (not due_tasks) and (not new_overdue_tasks):
                    old_overdue_tasks = []
                # Add tasks to lists for the group convenor
                all_due_tasks.extend(due_tasks)
                all_new_overdue_tasks.extend(new_overdue_tasks)
                all_old_overdue_tasks.extend(old_overdue_tasks)        
                # Send the email to the participant
                send_reminder_email(group, participant, reminder_interval,
                                    due_tasks, new_overdue_tasks,
                                    old_overdue_tasks)
            send_summary_email(group, reminder_interval, all_due_tasks, 
                               all_new_overdue_tasks, all_old_overdue_tasks)


def send_reminder_email(group, participant, reminder_interval, due_tasks,
                        new_overdue_tasks, old_overdue_tasks):
    """
    Emails a reminder about due and overdue tasks to the participants
    they are assigned to.
    """
    if due_tasks or new_overdue_tasks:
        first_name = participant.first_name
        group_name = group.name
        # Set up the email fields
        recipient = [participant.email]    
        sender = 'eConvenor <noreply@econvenor.org>'
        subject = group_name + ': Your tasks which are due soon or overdue'
        # Generate the email body
        body = 'Hi %s,\n' % first_name
        if new_overdue_tasks != []:
            body += '\nThese tasks were due yesterday and are now overdue:\n'
            for task in new_overdue_tasks:
                body += '* ' + task.description + '\n'   
        if due_tasks != []:
            body += '\nThese tasks are due in %s days or less:\n' % \
                    reminder_interval
            for task in due_tasks:
                deadline = task.deadline.strftime("%d %b %Y")
                body += '* ' + task.description + ' (due by ' + \
                        deadline + ')\n'    
        if old_overdue_tasks != []:
            body += '\nThese tasks have been overdue for more than a day:\n'
            for task in old_overdue_tasks:
                deadline = task.deadline.strftime("%d %b %Y")
                body += '* ' + task.description + ' (due by ' + \
                        deadline + ')\n'   
        body += '\neConvenor automatically emails you when a task ' + \
                'assigned to you is recorded as incomplete and it either ' + \
                'becomes due in 3 days, or becomes overdue.\n'
        body += '\nTo report tasks in this message as complete, email ' + \
                group.users.get().email     
        # Send the email
        email = EmailMessage(subject, body, sender, recipient,
                             bcc=['mail@econvenor.org'])
        email.send()


def send_summary_email(group, reminder_interval, all_due_tasks, 
                       all_new_overdue_tasks, all_old_overdue_tasks):
    """
    Emails a summary of the day's email notifications to
    the group convenor/s.
    """
    if all_due_tasks or all_new_overdue_tasks or all_old_overdue_tasks:
        user = group.users.get()
        first_name = user.first_name
        group_name = group.name
        # Set up the email fields
        recipient = [user.email]    
        sender = 'eConvenor <noreply@econvenor.org>'
        subject = group_name + ': Summary of today\'s automatic task \
                  notifications'
        # Generate the email body
        body = 'Hi %s,\n' % first_name
        body += '\neConvenor has just emailed reminders about these tasks' + \
                ' to the people responsible for them:\n'
        if all_due_tasks != []:
            body += '\nTasks which are due in the next %s days:\n' % reminder_interval
            for task in all_due_tasks:
                deadline = task.deadline.strftime("%d %b %Y")
                body += '* ' + task.description + ' (' + \
                        str(task.participant) + ' / due by ' + \
                        deadline + ')\n'
        if all_new_overdue_tasks != []:
            body += '\nTasks which were due yesterday and are now overdue:\n'
            for task in all_new_overdue_tasks:
                body += '* ' + task.description + ' (' + \
                        str(task.participant) + ')\n'  
        if all_old_overdue_tasks != []:
            body += '\nTasks which have been overdue for more than a day:\n'
            for task in all_old_overdue_tasks:
                deadline = task.deadline.strftime("%d %b %Y")
                body += '* ' + task.description + ' (' + \
                        str(task.participant) + ' / due by ' + deadline + ')\n'
        # Send the email
        email = EmailMessage(subject, body, sender, recipient,
                             bcc=['mail@econvenor.org'])
        email.send()
