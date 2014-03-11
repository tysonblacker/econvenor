from django import forms

from participants.models import Participant


class AddParticipantForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(AddParticipantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Participant
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone',
                  'notes',
                  ]

    def save(self, group, commit=True):
        participant = super(AddParticipantForm, self).save(commit=False)
        participant.group = group
        if commit:
            participant.save()
        return participant
        

class EditParticipantForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(EditParticipantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Participant
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone',
                  'notes',
                  'status',
                  'no_reminders',
                  ]

    def save(self, group, commit=True):
        participant = super(EditParticipantForm, self).save(commit=False)
        participant.group = group
        if commit:
            participant.save()
        return participant
