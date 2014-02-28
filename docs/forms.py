from django import forms

from docs.models import Item


class AgendaForm(forms.ModelForm):
    
    class Meta:
        model = Item
        widgets = {
		   	'background': forms.Textarea(attrs={'rows': 3}),
			'item_no': forms.HiddenInput(),
        }
        exclude = ('meeting', 'minute_notes', 'owner', )
        

class MinutesForm(forms.ModelForm):
    
    class Meta:
        model = Item
        exclude = ('editable', 'meeting', 'owner', 'show_tasks', )
