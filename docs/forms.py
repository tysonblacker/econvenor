from django import forms

from docs.models import Item


class AgendaForm(forms.ModelForm):
    
    class Meta:
        
        model = Item
        
        widgets = {
		   	'background': forms.Textarea(attrs={'rows': 3}),
		   	'item_no': forms.TextInput(attrs={'readonly': True, 'width': '50%'}),
        }
        
        exclude = ('meeting', 'minute_notes', 'owner', )
        
        def clean_item_no(self):
            return self.instance.item_no
             

class MinutesForm(forms.ModelForm):
    
    class Meta:
        model = Item
        exclude = ('editable', 'meeting', 'owner', 'show_tasks', )
