from django import forms

from decisions.models import Decision
        

class DecisionForm(forms.ModelForm):
    
    class Meta:
        model = Decision
        
