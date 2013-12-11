from django.contrib import admin
from core.models import Decision, Item, Meeting, Participant, Task


class ParticipantAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email_address', 'phone_number',)
	list_filter = ['first_name']

class TaskAdmin(admin.ModelAdmin):
	list_display = ('description', 'deadline', 'status',)
	list_filter = ['deadline']

class MeetingAdmin(admin.ModelAdmin):
	list_display = ('date', 'location', 'description')
	list_filter = ['date']

class ItemAdmin(admin.ModelAdmin):
	list_display = ('heading', 'background', 'variety')
	list_filter = ['heading']
	
class DecisionAdmin(admin.ModelAdmin):
    list_display = ('description',)
  

admin.site.register(Decision, DecisionAdmin)  
admin.site.register(Item, ItemAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Task, TaskAdmin)



