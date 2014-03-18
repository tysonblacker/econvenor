from django import forms

from participants.models import Participant
from tasks.models import Task


class AddTaskForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = \
            Participant.objects.filter(group=group)
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                  'notes',
                  ]
                  
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
            Participant.objects.filter(group=group)
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                  'status',
                  'completion_date',
                  'notes',
                  ]
                  
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
            Participant.objects.filter(group=group)
        
    class Meta:
        model = Task
        fields = ['description',
                  'participant',
                  'deadline',
                 ]
                  
    def save(self, group, commit=True):
        task = super(MinutesTaskForm, self).save(commit=False)
        task.group = group
        if commit:
            task.save()
        return task
