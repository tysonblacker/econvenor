from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views


admin.autodiscover()


urlpatterns = patterns('',

	url(r'^$', views.index, name='index'),
	url(r'^logout/$', views.user_logout, name="logout"),
	    
	url(r'^admin/', include(admin.site.urls)),
		
	url(r'^dashboard/$', views.dashboard, name="dashboard"),
    
	url(r'^participants/$', views.participant_list, name="participant-list"),
	url(r'^participant/add/$', views.participant_add, name="participant-add"),       
	url(r'^participant/(\d{1,4})/$', views.participant_view, name="participant-view"),
	url(r'^participant/(\d{1,4})/edit/$', views.participant_edit, name="participant-edit"),
	
	url(r'^tasks/$', views.task_list, name="task-list"),
	url(r'^task/add/$', views.task_add, name="task-add"),       
	url(r'^task/(\d{1,4})/edit/$', views.task_edit, name="task-edit"),
   	
	url(r'^agendas/$', views.agenda_list, name="agenda-list"),
	url(r'^agenda/add/$', views.agenda_add, name="agenda-add"),       
	url(r'^agenda/(\d{1,4})/edit/$', views.agenda_edit, name="agenda-edit"),       
	url(r'^agenda/(\d{1,4})/distribute/$', views.agenda_distribute, name="agenda-distribute"),       
	url(r'^agenda/(\d{1,4})/print/$', views.print_agenda, name="agenda-print"),
	
	url(r'^minutes/$', views.minutes_list, name="minutes-list"),
	url(r'^minutes/(\d{1,4})/edit/$', views.minutes_edit, name="minutes-edit"),

	url(r'^decisions/$', views.decision_list, name="decision-list"),
	
	url(r'^user-guide/$', views.user_guide, name="user-guide"),
	url(r'^faqs/$', views.faqs, name="faqs"),
	url(r'^ask-question/$', views.ask_question, name="ask-question"),
			
	url(r'^account-settings/$', views.account_settings, name="account-settings"),

	url(r'^bugs/$', views.bug_list, name="bug-list"),	
	url(r'^bugs/report/$', views.bug_report, name="bug-report"),
	url(r'^bugs/(\d{1,4})/edit/$', views.bug_edit, name="bug-edit"),       
	url(r'^features/$', views.feature_list, name="feature-list"),		
	url(r'^features/request/$', views.feature_request, name="feature-request"),
	url(r'^features/(\d{1,4})/edit/$', views.feature_edit, name="feature-edit"),       
		
)
