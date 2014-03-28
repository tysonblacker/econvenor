from django import forms

from decisions.models import Decision
        

class MinutesDecisionForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(MinutesDecisionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Decision
        
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '300 characters maximum',
                }),
            }            
        
    def save(self, group, commit=True):
        decision = super(MinutesDecisionForm, self).save(commit=False)
        decision.group = group
        if commit:
            decision.save()
        return decision
