from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', 'landing.views.index', name="index"),
	url(r'^login/$', 'core.views.user_login', name="login"),
	url(r'^logout/$', 'core.views.user_logout', name="logout"),
	    
	url(r'^admin/', include(admin.site.urls)),
		
	url(r'^dashboard/$', 'core.views.dashboard', name="dashboard"),
    
	url(r'^participants/$', 'core.views.participant_list', name="participant-list"),
	url(r'^participant/add/$', 'core.views.participant_add', name="participant-add"),       
	url(r'^participant/(\d{1,4})/$', 'core.views.participant_view', name="participant-view"),
	url(r'^participant/(\d{1,4})/edit/$', 'core.views.participant_edit', name="participant-edit"),
	
	url(r'^tasks/$', 'core.views.task_list', name="task-list"),
	url(r'^task/add/$', 'core.views.task_add', name="task-add"),       
	url(r'^task/(\d{1,4})/edit/$', 'core.views.task_edit', name="task-edit"),
   	
	url(r'^agendas/$', 'core.views.agenda_list', name="agenda-list"),
	url(r'^agenda/add/$', 'core.views.agenda_add', name="agenda-add"),       
	url(r'^agenda/(\d{1,4})/edit/$', 'core.views.agenda_edit', name="agenda-edit"),       
	url(r'^agenda/(\d{1,4})/distribute/$', 'core.views.agenda_distribute', name="agenda-distribute"),       
	url(r'^agenda/(\d{1,4})/print/$', 'core.views.agenda_print', name="agenda-print"),
	url(r'^agenda/(\d{1,4})/sent/$', 'core.views.agenda_sent', name="agenda-sent"),
		
	url(r'^minutes/$', 'core.views.minutes_list', name="minutes-list"),
	url(r'^minutes/(\d{1,4})/edit/$', 'core.views.minutes_edit', name="minutes-edit"),

	url(r'^decisions/$', 'core.views.decision_list', name="decision-list"),
	
	url(r'^user-guide/$', 'core.views.user_guide', name="user-guide"),
	url(r'^faqs/$', 'core.views.faqs', name="faqs"),
	url(r'^ask-question/$', 'core.views.ask_question', name="ask-question"),
			
	url(r'^account-settings/$', 'core.views.account_settings', name="account-settings"),

	url(r'^bugs/$', 'core.views.bug_list', name="bug-list"),	
	url(r'^bugs/report/$', 'core.views.bug_report', name="bug-report"),
	url(r'^bugs/(\d{1,4})/edit/$', 'core.views.bug_edit', name="bug-edit"),       
	url(r'^features/$', 'core.views.feature_list', name="feature-list"),		
	url(r'^features/request/$', 'core.views.feature_request', name="feature-request"),
	url(r'^features/(\d{1,4})/edit/$', 'core.views.feature_edit', name="feature-edit"),       
		
)
