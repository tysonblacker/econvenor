from django import forms

from docs.models import Item


class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
