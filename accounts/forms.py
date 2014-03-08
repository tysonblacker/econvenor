from django import forms

from accounts.models import Account

        
class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        widgets = {
        	'owner': forms.HiddenInput(),
        	'date_altered': forms.HiddenInput(),
        }
        

class AccountSetupForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('first_name', 'last_name')
