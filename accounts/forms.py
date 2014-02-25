from django import forms

from core.models import Account

        
class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        widgets = {
        	'owner': forms.HiddenInput(),
        	'date_altered': forms.HiddenInput(),
        }
        
 
