from django import forms

from participants.models import Participant


class ParticipantForm(forms.ModelForm):
    
    class Meta:
        model = Participant
        widgets = {
        	'owner': forms.HiddenInput(),
        }
        
