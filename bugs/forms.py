from django import forms

from bugs.models import Bug, Feature


class BugForm(forms.ModelForm):

    class Meta:
        model = Bug
        widgets = {
            'trigger': forms.Textarea(attrs={'rows': 3}),
            'goal': forms.Textarea(attrs={'rows': 3}),
            'behaviour': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            }
        fields = [
            'title',
            'location',
            'trigger',
            'goal',
            'behaviour',
            'comment',
            'status',
            'comment_closing',
            ]

    def save(self, user, commit=True):
        bug = super(BugForm, self).save(commit=False)
        try:
            bug.user = self.instance.user
        except:
            bug.user = user
        if commit:
            bug.save()
        return bug


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Feature
        widgets = {
            'goal': forms.Textarea(attrs={'rows': 3}),
            'shortcoming': forms.Textarea(attrs={'rows': 3}),
            'suggestion': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            }
        fields = [
            'title',
            'goal',
            'shortcoming',
            'suggestion',
            'comment',
            'status',
            'comment_closing',
            ]

    def save(self, user, commit=True):
        feature = super(FeatureForm, self).save(commit=False)
        try:
            feature.user = self.instance.user
        except:
            feature.user = user
        if commit:
            feature.save()
        return feature

