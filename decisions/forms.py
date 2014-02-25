from django import forms

from core.models import Decision
        

class DecisionForm(forms.ModelForm):
    
    class Meta:
        model = Decision
        
