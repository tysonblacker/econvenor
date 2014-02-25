from django import forms

from meetings.models import Meeting
from meetings.customwidgets import TimeSelectorWidget


class MeetingForm(forms.ModelForm):

	class Meta:
		model = Meeting
		widgets = {
        	'location': forms.Textarea(attrs={'rows': 3}),
        	'owner': forms.HiddenInput(),
        	'agenda_locked': forms.HiddenInput(),
        	'date': forms.DateInput(attrs={'class': 'datepicker'}),
        	'notes': forms.Textarea(attrs={'rows': 4}),
			'start_time': TimeSelectorWidget(),
        }


