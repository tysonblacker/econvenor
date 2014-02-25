from django import forms

from core.models import Participant


class ParticipantForm(forms.ModelForm):
    
    class Meta:
        model = Participant
        widgets = {
        	'owner': forms.HiddenInput(),
        }
        
