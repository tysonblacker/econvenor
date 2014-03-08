from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', 'landing.views.index', name="index"),
	url(r'^login/$', 'access.views.user_login', name="login"),
	url(r'^logout/$', 'access.views.user_logout', name="logout"),
	url(r'^register/$', 'access.views.user_register', name="register"),
		    
	url(r'^admin/', include(admin.site.urls)),
		
	url(r'^dashboard/$', 'dashboard.views.dashboard', name="dashboard"),
    
	url(r'^participants/$', 'participants.views.participant_list',
		name="participant-list"),
	url(r'^participant/add/$', 'participants.views.participant_add',
		name="participant-add"),       
	url(r'^participant/(\d{1,4})/$', 'participants.views.participant_view', name="participant-view"),
	url(r'^participant/(\d{1,4})/edit/$',
		'participants.views.participant_edit', name="participant-edit"),
	
	url(r'^tasks/$', 'tasks.views.task_list', name="task-list"),
	url(r'^task/add/$', 'tasks.views.task_add', name="task-add"),       
	url(r'^task/(\d{1,4})/edit/$', 'tasks.views.task_edit', name="task-edit"),
   	
	url(r'^agendas/$', 'docs.views.agenda_list', name="agenda-list"),
	url(r'^agenda/add/$', 'meetings.views.agenda_add', name="agenda-add"),       
	url(r'^agenda/(\d{1,4})/edit/$', 'docs.views.agenda_edit',
		name="agenda-edit"),       
	url(r'^agenda/(\d{1,4})/distribute/$', 'docs.views.agenda_distribute',
		name="agenda-distribute"),       
	url(r'^agenda/(\d{1,4})/print/$', 'docs.views.agenda_print',
		name="agenda-print"),
	url(r'^agenda/(\d{1,4})/sent/$', 'docs.views.agenda_sent',
		name="agenda-sent"),
		
	url(r'^minutes/$', 'docs.views.minutes_list', name="minutes-list"),
	url(r'^minutes/(\d{1,4})/edit/$', 'docs.views.minutes_edit',
		name="minutes-edit"),

	url(r'^decisions/$', 'decisions.views.decision_list',
		name="decision-list"),
	
	url(r'^user-guide/$', 'help.views.user_guide', name="user-guide"),
	url(r'^faqs/$', 'help.views.faqs', name="faqs"),
	url(r'^ask-question/$', 'help.views.ask_question', name="ask-question"),
			
	url(r'^account/$', 'accounts.views.account',
		name="account"),
	url(r'^account-setup/$', 'accounts.views.account_setup',
		name="account-setup"),

	url(r'^bugs/$', 'bugs.views.bug_list', name="bug-list"),	
	url(r'^bugs/report/$', 'bugs.views.bug_report', name="bug-report"),
	url(r'^bugs/(\d{1,4})/edit/$', 'bugs.views.bug_edit', name="bug-edit"),       
	url(r'^features/$', 'bugs.views.feature_list', name="feature-list"),		
	url(r'^features/request/$', 'bugs.views.feature_request',
		name="feature-request"),
	url(r'^features/(\d{1,4})/edit/$', 'bugs.views.feature_edit',
		name="feature-edit"),       
		
)   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


