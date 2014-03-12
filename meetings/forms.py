from django import forms

from meetings.models import Meeting
from meetings.customwidgets import TimeSelectorWidget


class AddMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(AddMeetingForm, self).__init__(*args, **kwargs)
                    
    class Meta:
        model = Meeting
        fields = ['meeting_no',
                  'meeting_type',
                  'date_scheduled',
                  'start_time_scheduled',
                  'location_scheduled',
                  'instructions_scheduled',
                  ]
        widgets = {
            'location_scheduled': forms.Textarea(attrs={'rows': 3}),
            'date_scheduled': forms.DateInput(attrs={'class': 'datepicker'}),
            'instructions_scheduled': forms.Textarea(attrs={'rows': 4}),
            'start_time_scheduled': TimeSelectorWidget(),
        }

    def save(self, group, commit=True):
        meeting = super(AddMeetingForm, self).save(commit=False)
        meeting.group = group
        meeting.status = 'Scheduled'
        if commit:
            meeting.save()
        return meeting


class MinutesMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(MinutesMeetingForm, self).__init__(*args, **kwargs)
                    
    class Meta:
        model = Meeting
        fields = ['date_actual',
                  'start_time_actual',
                  'end_time_actual',
                  'location_actual',
                  'instructions_actual',
                  ]
        widgets = {
            'location_actual': forms.Textarea(attrs={'rows': 3}),
            'date_actual': forms.DateInput(attrs={'class': 'datepicker'}),
            'instructions_actual': forms.Textarea(attrs={'rows': 4}),
            'start_time_actual': TimeSelectorWidget(),
            'end_time_actual': TimeSelectorWidget(),            
        }

    def save(self, group, commit=True):
        meeting = super(AddMeetingForm, self).save(commit=False)
        meeting.group = group
        meeting.status = 'Complete'
        if commit:
            meeting.save()
        return meeting
