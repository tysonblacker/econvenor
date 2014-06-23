from django import forms

from participants.models import Participant
from tasks.models import Task


class AddTaskForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = \
            Participant.lists.active().filter(group=group)

    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                  'notes',
                  ]

        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                'rows': 2,
                }),
            'participant': forms.Select(attrs={
                'class': 'form-control',
                }),
            'deadline': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                }),
            'notes': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 300,
                'rows': 4,
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
            Participant.lists.active().filter(group=group)
        EDIT_STATUS_CHOICES = (
            ('Incomplete', 'Incomplete'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        )
        self.fields['status'].choices = EDIT_STATUS_CHOICES

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
            'description': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                'rows': 2,
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
                'class': 'charactercounter form-control',
                'maxlength': 300,
                'rows': 4,
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
            Participant.lists.active().filter(group=group)
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                 ]
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'charactercounter form-control description-field',
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
