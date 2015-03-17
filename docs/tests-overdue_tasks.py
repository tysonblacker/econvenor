from datetime import date, timedelta

from django.test import TestCase

from docs.utils import get_completed_tasks_list, \
                       get_outstanding_tasks_list, \
                       get_overdue_tasks_list
from accounts.models import Group
from meetings.models import Meeting
from tasks.models import Task

today = date.today()
two_weeks_ago = today - timedelta(14)
one_week_ago = today - timedelta(7)
three_days_ago = today - timedelta(3)
yesterday = today - timedelta(1)
tomorrow = today + timedelta(1)
three_days_away = today + timedelta(3)
one_week_away = today + timedelta(7)
two_weeks_away = today + timedelta(14)

class TaskListsTests(TestCase):
    def setUp(self):
        TheGroup = Group.objects.create(name='TheGroup')
        TheMeeting = Meeting.objects.create(meeting_no='Mtg1', group_id=1)
        Task.objects.create(group=TheGroup,
                            meeting=TheMeeting,
                            description='TaskDueOneWeekAgo',
                            deadline=one_week_ago)
        Task.objects.create(group=TheGroup,
                            meeting=TheMeeting,
                            description='TaskDueYesterday',
                            deadline=yesterday)
        Task.objects.create(group=TheGroup,
                            meeting=TheMeeting,
                            description='TaskDueToday',
                            deadline=today)
        Task.objects.create(group=TheGroup,
                            meeting=TheMeeting,
                            description='TaskDueTomorrow',
                            deadline=tomorrow)
        Task.objects.create(group=TheGroup,
                            meeting=TheMeeting,
                            description='TaskDueInOneWeek',
                            deadline=one_week_away)

    def test_overdue_tasks_for_agendas(self):
        """
        The list of overdue tasks is correctly constructed for agendas.
        """
        ###############
        ##Set variables
        ###############
        TheGroup = Group.objects.get(name='TheGroup')
        TheMeeting = Meeting.objects.get(meeting_no='Mtg1', group_id=1)
        all_tasks = Task.objects.all()
        ######################
        ##Set tasks to 'Draft'
        ######################
        for task in all_tasks:
            task.status='Draft'
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ################################################
        ##Test draft tasks for a meeting scheduled today
        ################################################
        TheMeeting.date_scheduled = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##########################
        ##Set tasks to 'Cancelled'
        ##########################
        for task in all_tasks:
            task.status='Cancelled'
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ####################################################
        ##Test cancelled tasks for a meeting scheduled today
        ####################################################
        TheMeeting.date_scheduled = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ###########################
        ##Set tasks to 'Incomplete'
        ###########################
        for task in all_tasks:
            task.status='Incomplete'
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ###################################################
        ##Test incomplete tasks for a meeting two weeks ago
        ###################################################
        TheMeeting.date_scheduled = two_weeks_ago
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##################################################
        ##Test incomplete tasks for a meeting one week ago
        ##################################################
        TheMeeting.date_scheduled = one_week_ago
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##############################################################
        ##Test incomplete tasks for a meeting scheduled three days ago
        ##############################################################
        TheMeeting.date_scheduled = three_days_ago
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #########################################################
        ##Test incomplete tasks for a meeting scheduled yesterday
        #########################################################
        TheMeeting.date_scheduled = yesterday
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #####################################################
        ##Test incomplete tasks for a meeting scheduled today
        #####################################################
        TheMeeting.date_scheduled = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, True)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ########################################################
        ##Test incomplete tasks for a meeting scheduled tomorrow
        ########################################################
        TheMeeting.date_scheduled = tomorrow
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, True)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ###########################################################
        ##Test incomplete tasks for a meeting scheduled in one week
        ###########################################################
        TheMeeting.date_scheduled = one_week_away
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, True)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##############################
        ##Set tasks as completed today
        ##############################
        for task in all_tasks:
            task.status='Completed'
            task.completion_date = today
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ##########################################################
        ##Test tasks completed today for a meeting scheduled today
        ##########################################################
        TheMeeting.date_scheduled = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##############################################################
        ##Test tasks completed today for a meeting scheduled yesterday
        ##############################################################
        TheMeeting.date_scheduled = yesterday
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #############################################################
        ##Test tasks completed today for a meeting scheduled tomorrow
        #############################################################
        TheMeeting.date_scheduled = tomorrow
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##################################
        ##Set tasks as completed yesterday
        ##################################
        for task in all_tasks:
            task.status='Completed'
            task.completion_date = yesterday
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ##############################################################
        ##Test tasks completed yesterday for a meeting scheduled today
        ##############################################################
        TheMeeting.date_scheduled = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##################################################################
        ##Test tasks completed yesterday for a meeting scheduled yesterday
        ##################################################################
        TheMeeting.date_scheduled = yesterday
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ###################################################################
        ##Test tasks completed yesterday for a meeting scheduled 3 days ago
        ###################################################################
        TheMeeting.date_scheduled = three_days_ago
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='agenda')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)


    def test_overdue_tasks_for_minutes(self):
        """
        The list of overdue tasks is correctly constructed for minutes.
        """
        ###############
        ##Set variables
        ###############
        TheGroup = Group.objects.get(name='TheGroup')
        TheMeeting = Meeting.objects.get(meeting_no='Mtg1', group_id=1)
        all_tasks = Task.objects.all()
        ######################
        ##Set tasks to 'Draft'
        ######################
        for task in all_tasks:
            task.status='Draft'
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ######################################
        ##Test draft tasks for a meeting today
        ######################################
        TheMeeting.date_actual = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##########################
        ##Set tasks to 'Cancelled'
        ##########################
        for task in all_tasks:
            task.status='Cancelled'
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ##########################################
        ##Test cancelled tasks for a meeting today
        ##########################################
        TheMeeting.date_actual = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ###########################
        ##Set tasks to 'Incomplete'
        ###########################
        for task in all_tasks:
            task.status='Incomplete'
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ####################################################
        ##Test incomplete tasks for a meeting three days ago
        ####################################################
        TheMeeting.date_actual = three_days_ago
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ###############################################
        ##Test incomplete tasks for a meeting yesterday
        ###############################################
        TheMeeting.date_actual = yesterday
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ###########################################
        ##Test incomplete tasks for a meeting today
        ###########################################
        TheMeeting.date_actual = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, True)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##############################################
        ##Test incomplete tasks for a meeting tomorrow
        ##############################################
        TheMeeting.date_actual = tomorrow
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #################################################
        ##Test incomplete tasks for a meeting in one week
        #################################################
        TheMeeting.date_actual = one_week_away
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #################################
        ##Set tasks to as completed today
        #################################
        for task in all_tasks:
            task.status='Completed'
            task.completion_date = today
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ##############################################################
        ##Test tasks completed today for a meeting scheduled yesterday
        ##############################################################
        TheMeeting.date_actual = yesterday
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##########################################################
        ##Test tasks completed today for a meeting scheduled today
        ##########################################################
        TheMeeting.date_actual = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #############################################################
        ##Test tasks completed today for a meeting scheduled tomorrow
        #############################################################
        TheMeeting.date_actual = tomorrow
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        #####################################
        ##Set tasks to as completed yesterday
        #####################################
        for task in all_tasks:
            task.status='Completed'
            task.completion_date = yesterday
            task.save()
        task_due_one_week_ago = Task.objects.get(
                                   description='TaskDueOneWeekAgo')
        task_due_yesterday = Task.objects.get(
                                  description='TaskDueYesterday')
        task_due_today = Task.objects.get(
                         description='TaskDueToday')
        task_due_tomorrow = Task.objects.get(
                            description='TaskDueTomorrow')
        task_due_in_one_week = Task.objects.get(
                               description='TaskDueInOneWeek')
        ###################################################################
        ##Test tasks completed yesterday for a meeting scheduled 3 days ago
        ###################################################################
        TheMeeting.date_actual = three_days_ago
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, True)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##################################################################
        ##Test tasks completed yesterday for a meeting scheduled yesterday
        ##################################################################
        TheMeeting.date_actual = yesterday
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)
        ##############################################################
        ##Test tasks completed yesterday for a meeting scheduled today
        ##############################################################
        TheMeeting.date_actual = today
        TheMeeting.save()
        overdue_tasks = get_overdue_tasks_list(group=TheGroup,
                                              meeting=TheMeeting,
                                              doc_type='minutes')
        task_due_one_week_ago_included = task_due_one_week_ago in overdue_tasks
        self.assertEqual(task_due_one_week_ago_included, False)
        task_due_yesterday_included = task_due_yesterday in overdue_tasks
        self.assertEqual(task_due_yesterday_included, False)
        task_due_today_included = task_due_today in overdue_tasks
        self.assertEqual(task_due_today_included, False)
        task_due_tomorrow_included = task_due_tomorrow in overdue_tasks
        self.assertEqual(task_due_tomorrow_included, False)
        task_due_in_one_week_included = task_due_in_one_week in overdue_tasks
        self.assertEqual(task_due_in_one_week_included, False)

