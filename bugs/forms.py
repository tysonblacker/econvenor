from django import forms

from core.models import Bug, Feature

       
class BugForm(forms.ModelForm):

	class Meta:
		model = Bug
		widgets = {
		   	'trigger': forms.Textarea(attrs={'rows': 3}),
		   	'behaviour': forms.Textarea(attrs={'rows': 3}),
		   	'goal': forms.Textarea(attrs={'rows': 3}),
			'owner': forms.HiddenInput(),
			'date': forms.HiddenInput(),
        }


class FeatureForm(forms.ModelForm):

	class Meta:
		model = Feature
		widgets = {
			'goal': forms.Textarea(attrs={'rows': 3}),
			'shortcoming': forms.Textarea(attrs={'rows': 3}),
			'suggestion': forms.Textarea(attrs={'rows': 3}),
			'owner': forms.HiddenInput(),
			'date': forms.HiddenInput(),
        }

