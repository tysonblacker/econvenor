from django import forms

from participants.models import Participant
from tasks.models import Task


class TaskForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = Participant.objects.filter(owner=user)
        
    class Meta:
        model = Task
        widgets = {
        	'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        	'deadline': forms.DateInput(attrs={'class': 'datepicker'}),
        	'status': forms.Select(attrs={'class': 'form-control'}),
        	'owner': forms.HiddenInput(),
        	'meeting': forms.HiddenInput(),
        	'item': forms.HiddenInput(),
        }

