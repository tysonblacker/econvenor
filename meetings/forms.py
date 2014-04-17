from django import forms

from django.utils.translation import ugettext, ugettext_lazy as _

from meetings.models import Meeting
from participants.models import Participant


class NewMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        self.group = group
        super(NewMeetingForm, self).__init__(*args, **kwargs)
        self.fields['facilitator_scheduled'].queryset = \
            Participant.lists.active().filter(group=group)
        self.fields['minute_taker_scheduled'].queryset = \
            Participant.lists.active().filter(group=group)
            
    error_messages = {
        'duplicate_meeting_no': _('That meeting number has already been used.'\
        ' Please choose a different one.'),
    }

                    
    class Meta:
        model = Meeting
        fields = ['meeting_no',
                  'meeting_type',
                  'date_scheduled',
                  'start_time_scheduled',
                  'location_scheduled',
                  'facilitator_scheduled',
                  'minute_taker_scheduled',
                  'instructions_scheduled',
                  ]
        widgets = {
            'meeting_no': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                'placeholder': 'e.g. \'Mtg4/2014\' or \'June 2014\'',
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
                'class': 'charactercounter form-control',
                'maxlength': 60,
                'rows': 2,
                }),
            'facilitator_scheduled': forms.Select(attrs={
                'class': 'form-control',
                }),
            'minute_taker_scheduled': forms.Select(attrs={
                'class': 'form-control',
                }),
            'instructions_scheduled': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 200,
                'rows': 4,
                }),
            }
        labels = {
            'meeting_no': 'Meeting name or number '
                          '(must be unique for each meeting)',
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
        meeting = super(NewMeetingForm, self).save(commit=False)
        meeting.group = group
        meeting.status = 'Scheduled'
        if commit:
            meeting.save()
        return meeting


class AgendaMeetingForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        self.group = group
        super(AgendaMeetingForm, self).__init__(*args, **kwargs)
        self.fields['facilitator_scheduled'].queryset = \
            Participant.lists.active().filter(group=group)
        self.fields['minute_taker_scheduled'].queryset = \
            Participant.lists.active().filter(group=group)

            
    error_messages = {
        'duplicate_meeting_no': _('That meeting number has already been used.'\
        ' Please choose a different one.'),
    }
                    
    class Meta:
        model = Meeting
        fields = ['meeting_no',
                  'meeting_type',
                  'date_scheduled',
                  'start_time_scheduled',
                  'location_scheduled',
                  'facilitator_scheduled',
                  'minute_taker_scheduled',
                  'instructions_scheduled',
                  ]
        widgets = {
            'meeting_no': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
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
                'class': 'charactercounter form-control',
                'maxlength': 60,
                'rows': 2,
                }),
            'facilitator_scheduled': forms.Select(attrs={
                'class': 'form-control',
                }),
            'minute_taker_scheduled': forms.Select(attrs={
                'class': 'form-control',
                }),
            'instructions_scheduled': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 200,
                'rows': 4,
                }),
            }
        labels = {
            'meeting_no': 'Meeting name or number '
                          '(unique)',
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
            Participant.lists.active().filter(group=group)
        self.fields['minute_taker_actual'].queryset = \
            Participant.lists.active().filter(group=group)
                    
    class Meta:
        model = Meeting
        fields = ['date_actual',
                  'start_time_actual',
                  'end_time_actual',
                  'location_actual',
                  'facilitator_actual',
                  'minute_taker_actual',
                  'attendance',
                  'apologies',
                  'instructions_actual',
                  ]
        widgets = {
            'date_actual': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'start_time_actual': forms.TimeInput(attrs={
                'class': 'timepicker form-control',
                }),
            'end_time_actual': forms.TimeInput(attrs={
                'class': 'timepicker form-control',
                }),
            'location_actual': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 60,
                'rows': 2,
                }),
            'facilitator_actual': forms.Select(attrs={
                'class': 'form-control',
                }),
            'minute_taker_actual': forms.Select(attrs={
                'class': 'form-control',
                }),
            'attendance': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 500,
                'rows': 4,
                }),
            'apologies': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 200,
                'rows': 3,
                }),
            'instructions_actual': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 200,
                'rows': 4,
                }),
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
            Participant.lists.active().filter(group=group)
        self.fields['next_meeting_minute_taker'].queryset = \
            Participant.lists.active().filter(group=group)
                                  
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
            'next_meeting_date': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'next_meeting_start_time': forms.TimeInput(attrs={
                'class': 'timepicker form-control',
                }),
            'next_meeting_location': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 60,
                'rows': 2,
                }),
            'next_meeting_facilitator': forms.Select(attrs={
                'class': 'form-control',
                }),
            'next_meeting_minute_taker': forms.Select(attrs={
                'class': 'form-control',
                }),
            'next_meeting_instructions': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 200,
                'rows': 4,
                }),
            }       

    def save(self, group, commit=True):
        meeting = super(NextMeetingForm, self).save(commit=False)
        meeting.group = group
        if commit:
            meeting.save()
        return meeting
