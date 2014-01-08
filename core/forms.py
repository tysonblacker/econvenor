from django import forms

from core.models import Account, Decision, Item, Meeting, Participant, Task


class MeetingForm(forms.ModelForm):
        
    class Meta:
        model = Meeting
        widgets = {
        	'location': forms.Textarea(attrs={'rows': 3}),
        	'owner': forms.HiddenInput(),
        	'agenda_locked': forms.HiddenInput(),
        	'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        

class DecisionForm(forms.ModelForm):
    
    class Meta:
        model = Decision
        

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


class ParticipantForm(forms.ModelForm):
    
    class Meta:
        model = Participant
        widgets = {
        	'owner': forms.HiddenInput(),
        }
        
        
class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        widgets = {
        	'owner': forms.HiddenInput(),
        	'join_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
