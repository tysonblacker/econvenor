from django import forms

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from accounts.models import Group


class PasswordChangeForm(forms.ModelForm):
    """
    A form which changes a user's password.
    """
    error_messages = {
        'password_incorrect': _("The current password is incorrect"),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.RegexField(label=_("New password"), min_length=8,
        regex=r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*\W)[a-zA-Z0-9\S]{8,}$',
        widget=forms.PasswordInput(attrs={
                                   'class': 'form-control field-medium',
                                   }),
        error_messages={
            'invalid': _("Passwords must be at least 8 characters long and "
                         "include at least 1 digit and 1 special character.")})
    password2 = forms.CharField(label=_("Confirm new password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control field-medium',
                                   }))

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.user = user
    
    class Meta:
        model = User
        fields = ("password",)
        labels = {
            'password': _('Current password'),
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control field-medium',
                }),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        correct_password = check_password(password, self.user.password)
        if not correct_password:
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return password
   
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
            
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user


class GroupRegisterForm(forms.ModelForm):
    """
    A form that sets up basic user information once an account has been
    created. Is displayed with UserSetupForm on the one page.
    """
    error_messages = {
        'name_blank': _("You must enter the name of your group."),
    }
    name = forms.CharField(label=_("Group name"), max_length=100,
        help_text=_("Required. 100 characters or fewer."))
        
    class Meta:
        model = Group
        fields = ('name', 'aim', 'focus', 'country')
        help_texts = {
            'aim': _('A short statement of your group\'s main aim '
                     '(100 characters max.)'),
            'focus': _('e.g. refugee rights, climate change '
                       '(40 characters max.)'),
            'country': _('Your main country of operation '
                         '(40 characters max.)'),
        }

        
    def clean_name(self):
        name = self.cleaned_data["name"]
        if name == '':
            raise forms.ValidationError(
                self.error_messages['name_blank'],
                code='name_blank',
            )
        return name
