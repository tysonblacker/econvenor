from django import forms

from docs.models import Item


class AgendaItemForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(AgendaItemForm, self).__init__(*args, **kwargs)

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
        item = super(AgendaItemForm, self).save(commit=False)
        item.group = group
        if commit:
            item.save()
        return item
        
        
class MinutesItemForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(MinutesItemForm, self).__init__(*args, **kwargs)
            
    class Meta:
        model = Item
        fields = ['item_no',
                  'title',
                  'time_limit',
                  'explainer',
                  'background',
                  'minute_notes',
                  ]
        widgets = {
            'item_no': forms.HiddenInput(),
        }    

    def clean_id(self):
        return self.instance.id
        
    def clean_item_no(self):
        return self.instance.item_no
        
    def clean_title(self):
        return self.instance.title
    
    def clean_time_limit(self):
        return self.instance.time_limit

    def clean_explainer(self):
        return self.instance.explainer
        
    def clean_background(self):
        return self.instance.background                
                                            
    def save(self, group, commit=True):
        item = super(MinutesItemForm, self).save(commit=False)
        item.group = group
        if commit:
            item.save()
        return item
        
        
