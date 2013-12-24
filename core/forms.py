from django import forms


from core.models import Decision, Item, Meeting, Participant, Task


class MeetingForm(forms.ModelForm):
    
    class Meta:
        model = Meeting


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
        	'deadline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deadline'}),
        	'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status'}),
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
