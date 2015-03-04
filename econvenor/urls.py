import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from accounts.forms import PasswordResetForm

admin.autodiscover()

ADMIN_URL = os.environ['ECONVENOR_ADMIN_URL'] + '/'

urlpatterns = patterns('',

    url(ADMIN_URL, include(admin.site.urls)),

    url(r'^$', 'landing.views.index', name="index"),
    url(r'^examples/example-agenda/$', 'landing.views.example_agenda',
        name="example-agenda"),
    url(r'^examples/example-minutes/$', 'landing.views.example_minutes',
        name="example-minutes"),
    url(r'^questions/$', 'landing.views.questions', name="questions"),
    url(r'^terms/$', 'landing.views.terms', name="terms"),
    url(r'^project/$', 'landing.views.project', name="project"),
    url(r'^contact/$', 'landing.views.contact', name="contact"),
    url(r'^volunteer/$', 'landing.views.volunteer', name="volunteer"),
    url(r'^donate/$', 'landing.views.donate', name="donate"),
    url(r'^hack/$', 'landing.views.hack', name="hack"),
    url(r'^conduct/$', 'landing.views.conduct', name="conduct"),
    url(r'^source/$', 'landing.views.source', name="source"),
    url(r'^pricing/$', 'landing.views.pricing', name="pricing"),
    url(r'^public-key/$', TemplateView.as_view(
        template_name='econvenor_public_key.txt',
        content_type='text/plain'
        ),name="public-key"),

    url(r'^login/$', 'authentication.views.user_login', name="login"),
    url(r'^logout/$', 'authentication.views.user_logout', name="logout"),

    url(r'^qualify/(step\d[a]?)/$', 'registration.views.qualify',
        name="qualify"),
    url(r'^register/(\w*)$', 'registration.views.register',
        name="register"),
    url(r'^welcome/$', 'registration.views.welcome', name="welcome"),

    url(r'^dashboard/$', 'dashboard.views.dashboard', name="dashboard"),
    url(r'^dashboard-admin/$', 'dashboard.views.dashboard_admin',
        name="dashboard-admin"),

    url(r'^participants/$', 'participants.views.participant_list',
        name="participant-list"),
    url(r'^participant/add/$', 'participants.views.participant_add',
        name="participant-add"),
    url(r'^participant/(\d{1,4})/$', 'participants.views.participant_view',
        name="participant-view"),
    url(r'^participant/(\d{1,4})/edit/$',
        'participants.views.participant_edit', name="participant-edit"),

    url(r'^my-tasks/(?P<participant_id>\d{1,4})/(?P<token>[0-9a-f]{40})/$',
        'participants.views.my_tasks_auth',
        name="my-tasks-auth"),
    url(r'^my-tasks/$', 'participants.views.my_tasks',
        name="my-tasks"),
    url(r'^my-tasks/done/$',
        'participants.views.my_tasks_done',
        name="my-tasks-done"),

    url(r'^tasks/$', 'tasks.views.task_list', name="task-list"),
    url(r'^tasks/add/$', 'tasks.views.task_add', name="task-add"),
    url(r'^tasks/(\d{1,4})/edit/$', 'tasks.views.task_edit', name="task-edit"),

    url(r'^meetings/archive/$', 'meetings.views.meeting_list_archive',
        name="meeting-list-archive"),
    url(r'^meetings/current/$', 'meetings.views.meeting_list_current',
        name="meeting-list-current"),
    url(r'^meetings/add/$', 'meetings.views.meeting_add', name="meeting-add"),

    url(r'^agenda/(\d{1,4})/edit/$', 'docs.views.agenda_edit',
        name="agenda-edit"),
    url(r'^agenda/(\d{1,4})/distribute/$', 'docs.views.agenda_distribute',
        name="agenda-distribute"),
    url(r'^agenda/(\d{1,4})/view/$', 'docs.views.agenda_view',
        name="agenda-view"),
    url(r'^agenda/(\d{1,4})/print/$', 'docs.views.agenda_print',
        name="agenda-print"),
    url(r'^agenda/(\d{1,4})/sent/$', 'docs.views.agenda_sent',
        name="agenda-sent"),

    url(r'^minutes/(\d{1,4})/edit/$', 'docs.views.minutes_edit',
        name="minutes-edit"),
    url(r'^minutes/(\d{1,4})/distribute/$', 'docs.views.minutes_distribute',
        name="minutes-distribute"),
    url(r'^minutes/(\d{1,4})/view/$', 'docs.views.minutes_view',
        name="minutes-view"),
    url(r'^minutes/(\d{1,4})/print/$', 'docs.views.minutes_print',
        name="minutes-print"),
    url(r'^minutes/(\d{1,4})/sent/$', 'docs.views.minutes_sent',
        name="minutes-sent"),

    url(r'^decisions/$', 'decisions.views.decision_list',
        name="decision-list"),

    url(r'^quick-start-guide/$', 'help.views.quick_start_guide',
        name="quick-start-guide"),
    url(r'^user-guide/$', 'help.views.user_guide', name="user-guide"),
    url(r'^qanda/$', 'help.views.qanda', name="qanda"),
    url(r'^ask-question/$', 'help.views.ask_question', name="ask-question"),

    url(r'^account/$', 'accounts.views.account', name="account"),
    url(r'^account/change-password/$', 'accounts.views.password_change',
        name="password-change"),
    url(r'^account/password-changed/$', 'accounts.views.password_changed',
        name="password-changed"),
    url(r'^account/edit-user-details/$', 'accounts.views.user_edit',
        name="user-edit"),
    url(r'^account/edit-group-details/$', 'accounts.views.group_edit',
        name="group-edit"),

    url(r'^bugs/$', 'bugs.views.bug_list', name="bug-list"),
    url(r'^bugs/report/$', 'bugs.views.bug_report', name="bug-report"),
    url(r'^bugs/(\d{1,4})/edit/$', 'bugs.views.bug_edit', name="bug-edit"),
    url(r'^bugs-admin/$', 'bugs.views.bug_list_admin', name="bug-list-admin"),
    url(r'^features/$', 'bugs.views.feature_list', name="feature-list"),
    url(r'^features/request/$', 'bugs.views.feature_request',
        name="feature-request"),
    url(r'^features/(\d{1,4})/edit/$', 'bugs.views.feature_edit',
        name="feature-edit"),
    url(r'^features-admin/$', 'bugs.views.feature_list_admin',
        name="feature-list-admin"),

    url(r'^forgotten-password/reset-request/$',
        'django.contrib.auth.views.password_reset',
        {
            'template_name':'password_reset.html',
            'email_template_name':'password_reset_email.html',
            'subject_template_name':'password_reset_subject.txt',
            'from_email':'noreply@econvenor.org',
        },
        name='password_reset'),
    url(r'^forgotten-password/email-sent/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name':'password_reset_done.html'},
        name='password_reset_done'),
    url(r'^forgotten-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'set_password_form':PasswordResetForm,
            'template_name':'password_reset_confirm.html',
        },
        name='password_reset_confirm'),
    url(r'^forgotten-password/reset-succeeded/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name':'password_reset_complete.html'},
        name='password_reset_complete'),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
        content_type='text/plain')),

)   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
