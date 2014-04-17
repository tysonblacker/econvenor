from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from docs.models import Item
from participants.models import Participant


class AgendaItemForm(forms.ModelForm):
    
    def __init__(self, group, *args, **kwargs):
        super(AgendaItemForm, self).__init__(*args, **kwargs)
        self.fields['explainer'].queryset = \
            Participant.lists.active().filter(group=group)

    class Meta:
        
        model = Item
        fields = ['item_no',
                  'title',
                  'time_limit',
                  'explainer',
                  'background'
                  ]
        widgets = {
            'item_no': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'charactercounter form-control item-title',
                }),
            'time_limit': forms.Select(attrs={
                'class': 'form-control',
                }),
            'explainer': forms.Select(attrs={
                'class': 'form-control',
                }),
            'background': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 1000,
                'rows': 3,
                }),
            }              
        labels = {
            'title': _('Item title'),
            'time_limit': _('Time limit (recommended)'),
            'explainer': _('To be explained by (optional)'),
            'background': _('Background information (optional)'),
        }

       
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
        self.fields['explainer'].queryset = \
            Participant.lists.active().filter(group=group)
       
    class Meta:
        model = Item
        fields = ['added_in_meeting',
                  'item_no',
                  'title',
                  'time_limit',
                  'explainer',
                  'background',
                  'minute_notes',
                  ]
        widgets = {
            'item_no': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'charactercounter form-control item-title',
                }),
            'minute_notes': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 2000,
                'rows': 4,
                }),
            }    
        labels = {
            'title': _('Item title'),
            'explainer': _('To be explained by'),
            'background': _('Background information'),
        }

    def clean_added_in_meeting(self):
        return self.instance.added_in_meeting

    def clean_id(self):
        return self.instance.id
        
    def clean_item_no(self):
        return self.instance.item_no
        
    def clean_title(self):
        if self.cleaned_data["title"] != '':
            return self.cleaned_data["title"]
        else:
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
        
        
