from django import forms

from participants.models import Participant
from tasks.models import Task


class AddTaskForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = \
            Participant.objects.filter(group=group, status='Active')
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                  'notes',
                  ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': '80 characters maximum',
                }),
            'participant': forms.Select(attrs={
                'class': 'form-control',
                }),
            'deadline': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': '300 characters maximum',
                }),
            }
                  
    def save(self, group, commit=True):
        task = super(AddTaskForm, self).save(commit=False)
        task.group = group
        if commit:
            task.save()
        return task
        
        
class EditTaskForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = \
            Participant.objects.filter(group=group, status='Active')
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                  'status',
                  'completion_date',
                  'notes',
                  ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': '80 characters maximum',
                }),
            'participant': forms.Select(attrs={
                'class': 'form-control',
                }),
            'deadline': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                }),
            'completion_date': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': '300 characters maximum',
                }),
            }

    def save(self, group, commit=True):
        task = super(EditTaskForm, self).save(commit=False)
        task.group = group
        if commit:
            task.save()
        return task
        
        
class MinutesTaskForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(MinutesTaskForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = \
            Participant.objects.filter(group=group, status='Active')
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                 ]
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control description-field',
                'placeholder': 'Description',
                }),
            'participant': forms.Select(attrs={
                'class': 'form-control participant-field',
                }),
            'deadline': forms.DateInput(attrs={
                'class': 'datepicker form-control deadline-field',
                'placeholder': 'Deadline',
                }),
            }

                  
    def save(self, group, commit=True):
        task = super(MinutesTaskForm, self).save(commit=False)
        task.group = group
        task.status = 'Draft'
        if commit:
            task.save()
        return task
