from django import forms

from django.utils.translation import ugettext, ugettext_lazy as _

from meetings.models import Meeting
from participants.models import Participant


class AgendaMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        self.group = group
        super(AgendaMeetingForm, self).__init__(*args, **kwargs)
        self.fields['facilitator_scheduled'].queryset = \
            Participant.objects.filter(group=group)
        self.fields['minute_taker_scheduled'].queryset = \
            Participant.objects.filter(group=group)

            
    error_messages = {
        'duplicate_meeting_no': _("That meeting number has already been used. please choose a different one."),
    }
                    
    class Meta:
        model = Meeting
        fields = ['meeting_no',
                  'meeting_type',
                  'date_scheduled',
                  'start_time_scheduled',
                  'location_scheduled',
                  'meeting_status',
                  'facilitator_scheduled',
                  'minute_taker_scheduled',
                  'instructions_scheduled',
                  ]
        widgets = {
            'meeting_no': forms.TextInput(attrs={
                'class': 'form-control',
                }),
            'meeting_type': forms.Select(attrs={
                'class': 'form-control',
                }),
            'date_scheduled': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'start_time_scheduled': forms.TimeInput(attrs={
                'class': 'timepicker form-control',
                }),
            'location_scheduled': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                }),
            'meeting_status': forms.Select(attrs={
                'class': 'form-control',
                }),
            'facilitator_scheduled': forms.Select(attrs={
                'class': 'form-control',
                }),
            'minute_taker_scheduled': forms.Select(attrs={
                'class': 'form-control',
                }),
            'instructions_scheduled': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                }),
            }
    
    def clean_meeting_no(self):
        meeting_no = self.cleaned_data["meeting_no"]
        this_meeting = self.instance.meeting_no
        try:
            Meeting._default_manager.get(meeting_no=meeting_no, group=self.group)
            other_meetings = Meeting._default_manager.\
            filter(meeting_no=meeting_no, group=self.group).\
            exclude(meeting_no=this_meeting)
        except Meeting.DoesNotExist:
            return meeting_no
        if other_meetings.count() == 0:
            return meeting_no
        else:
            raise forms.ValidationError(
                self.error_messages['duplicate_meeting_no'],
                code='duplicate_meeting_no',
                )

    def save(self, group, commit=True):
        meeting = super(AgendaMeetingForm, self).save(commit=False)
        meeting.group = group
        if commit:
            meeting.save()
        return meeting


class MinutesMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(MinutesMeetingForm, self).__init__(*args, **kwargs)
        self.fields['facilitator_actual'].queryset = \
            Participant.objects.filter(group=group)
        self.fields['minute_taker_actual'].queryset = \
            Participant.objects.filter(group=group)
                    
    class Meta:
        model = Meeting
        fields = ['date_actual',
                  'start_time_actual',
                  'end_time_actual',
                  'location_actual',
                  'instructions_actual',
                  'facilitator_actual',
                  'minute_taker_actual',
                  'attendance',
                  'apologies',
                  ]
        widgets = {
            'location_actual': forms.Textarea(attrs={'rows': 3}),
            'date_actual': forms.DateInput(attrs={'class': 'datepicker'}),
            'instructions_actual': forms.Textarea(attrs={'rows': 4}),
           'start_time_actual': forms.TimeInput(attrs=
                {'class': 'timepicker'}
            ),
           'end_time_actual': forms.TimeInput(attrs=
                {'class': 'timepicker'}
            ),
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
        self.fields['next_meeting_facilitator'].queryset = \
            Participant.objects.filter(group=group)
        self.fields['next_meeting_minute_taker'].queryset = \
            Participant.objects.filter(group=group)
                                  
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
            'next_meeting_start_time': forms.TimeInput(attrs=
                {'class': 'timepicker'}
            ),
        }

    def save(self, group, commit=True):
        meeting = super(NextMeetingForm, self).save(commit=False)
        meeting.group = group
        if commit:
            meeting.save()
        return meeting
