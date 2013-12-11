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
    
    class Meta:
        model = Task
        widgets = {
        	'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        	'deadline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deadline'}),
        	'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }


class ParticipantForm(forms.ModelForm):
    
    class Meta:
        model = Participant
