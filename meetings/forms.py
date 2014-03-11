from django import forms

from meetings.models import Meeting, MeetingDetails
from meetings.customwidgets import TimeSelectorWidget


class AddMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(AddMeetingForm, self).__init__(*args, **kwargs)
                    
    class Meta:
        model = Meeting
        fields = ['meeting_no',
                  'meeting_type',
                 ]

    def save(self, group, commit=True):
        meeting = super(AddMeetingForm, self).save(commit=False)
        meeting.group = group
        if commit:
            meeting.save()
        return meeting


class AddMeetingDetailsForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(AddMeetingDetailsForm, self).__init__(*args, **kwargs)
                    
    class Meta:
        model = MeetingDetails
        fields = ['date',
                  'start_time',
                  'location',
                  'instructions',
                  ]
        widgets = {
            'location': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'instructions': forms.Textarea(attrs={'rows': 4}),
            'start_time': TimeSelectorWidget(),
        }

    def save(self, group, commit=True):
        meeting_details = super(AddMeetingDetailsForm, self).save(commit=False)
        meeting_details.group = group
        meeting_details.details_type = 'scheduled'
        if commit:
            meeting_details.save()
        return meeting_details
