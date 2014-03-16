from django import forms

from meetings.models import Meeting
from meetings.customwidgets import TimeSelectorWidget


class AgendaMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(AgendaMeetingForm, self).__init__(*args, **kwargs)
                    
    class Meta:
        model = Meeting
        fields = ['meeting_no',
                  'meeting_type',
                  'date_scheduled',
                  'start_time_scheduled',
                  'location_scheduled',
                  'meeting_status',
                  'instructions_scheduled',
                  'facilitator_scheduled',
                  'minute_taker_scheduled',
                  ]
        widgets = {
            'location_scheduled': forms.Textarea(attrs={'rows': 3}),
            'date_scheduled': forms.DateInput(attrs={'class': 'datepicker'}),
            'instructions_scheduled': forms.Textarea(attrs={'rows': 4}),
            'start_time_scheduled': TimeSelectorWidget(),
        }

    def save(self, group, commit=True):
        meeting = super(AgendaMeetingForm, self).save(commit=False)
        meeting.group = group
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
                  'facilitator_scheduled',
                  'minute_taker_scheduled',
                  'attendance',
                  'apologies',
                  ]
        widgets = {
            'location_actual': forms.Textarea(attrs={'rows': 3}),
            'date_actual': forms.DateInput(attrs={'class': 'datepicker'}),
            'instructions_actual': forms.Textarea(attrs={'rows': 4}),
            'start_time_actual': TimeSelectorWidget(),
            'end_time_actual': TimeSelectorWidget(),            
        }

    def save(self, group, commit=True):
        meeting = super(MinutesMeetingForm, self).save(commit=False)
        meeting.group = group
        meeting.status = 'Complete'
        if commit:
            meeting.save()
        return meeting


class NextMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(NextMeetingForm, self).__init__(*args, **kwargs)
                      
    class Meta:
        model = Meeting
        fields = ['next_meeting_date',
                  'next_meeting_start_time',
                  'next_meeting_location',
                  'next_meeting_facilitator',
                  'next_meeting_minute_taker',
                  'next_meeting_instructions',
                  ]
        widgets = {
            'next_meeting_location': forms.Textarea(attrs={'rows': 3}),
            'next_meeting_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'next_meeting_instructions': forms.Textarea(attrs={'rows': 4}),
            'next_meeting_start_time': TimeSelectorWidget(),
        }

    def save(self, group, commit=True):
        meeting = super(NextMeetingForm, self).save(commit=False)
        meeting.group = group
        if commit:
            meeting.save()
        return meeting

