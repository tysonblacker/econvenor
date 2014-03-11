from django import forms

from docs.models import Item


class AgendaForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)
        
    class Meta:
        
        model = Item
        
        widgets = {
		   	'background': forms.Textarea(attrs={'rows': 3}),
        }
        
        fields = ['item_no',
                   'title',
                   'time_limit',
                   'explainer',
                   'background'
                   ]
        
    def clean_item_no(self):
        return self.instance.item_no
             
    def save(self, group, commit=True):
        item = super(AgendaForm, self).save(commit=False)
        item.group = group
        if commit:
            item.save()
        return item
        
        
class MinutesForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(MinutesForm, self).__init__(*args, **kwargs)
            
    class Meta:
        model = Item
        fields = ['item_no',
                   'title',
                   'time_limit',
                   'explainer',
                   'background'
                   ]
