from django import forms

from decisions.models import Decision
        

class MinutesDecisionForm(forms.ModelForm):
    
    class Meta:
        model = Decision
        
