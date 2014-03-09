from django import forms

from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from accounts.models import Group

        
class UserSetupForm(forms.ModelForm):
    """
    A form that sets up basic user information once an account has been
    created. Is displayed with GroupSetupForm on the one page.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists. "
                                "Please try again."),
    }
    username = forms.RegexField(label=_("Username"), min_length=2, max_length=30,
        regex=r'^[\w]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "underscores ('_') only."),
        error_messages={
            'invalid': _("You username may contain only letters, numbers and "
                         "underscore ('_') characters.")})
                                 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

class GroupSetupForm(forms.ModelForm):
    """
    A form that sets up basic user information once an account has been
    created. Is displayed with UserSetupForm on the one page.
    """
    error_messages = {
        'name_blank': _("You must enter the name of your group."),
    }
    name = forms.CharField(label=_("Group name"), max_length=70,
        help_text=_("Required. 70 characters or fewer."))
        
    class Meta:
        model = Group
        fields = ('name', 'description',)
        
    def clean_name(self):
        name = self.cleaned_data["name"]
        if name == '':
            raise forms.ValidationError(
                self.error_messages['name_blank'],
                code='name_blank',
            )
        return name
