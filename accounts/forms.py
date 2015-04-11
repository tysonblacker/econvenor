from django import forms

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from accounts.models import Group


class BasePasswordForm(forms.ModelForm):
    """
    A base class to use for PasswordChangeForm and PasswordResetForm.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_incorrect': _("The current password is incorrect"),
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
        super(BasePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

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


class PasswordResetForm(BasePasswordForm):
    """
    A form which resets a user's password when the user is not logged in to
    eConvenor.
    """
    class Meta:
        model = User
        fields = []


class PasswordChangeForm(BasePasswordForm):
    """
    A form which changes a user's password when the user is logged in to
    eConvenor.
    """

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


class UserDetailsForm(forms.ModelForm):
    """
    A form that allows a user to edit their details.
    """
    error_messages = {
        'duplicate_email': _("A user with that email address already exists. "
                             "Please try again."),
        'duplicate_username': _("A user with that username already exists. "
                                "Please try again."),
    }
    email = forms.EmailField(label=_("Email address"),
        widget=forms.EmailInput(attrs={
                                   'class': 'form-control field-medium email',
                                   }),
        error_messages={
            'invalid': _("This must be a valid email address.")})
    username = forms.RegexField(label=_("Preferred username"), min_length=2,
                                max_length=30,
        regex=r'^[\w]+$',
        widget=forms.TextInput(attrs={
                                   'class': 'form-control field-medium',
                                   }),
        help_text=_("30 characters or fewer. Letters, digits and underscores "
                    "('_') only."),
        error_messages={
            'invalid': _("You username may contain only letters, numbers and "
                         "underscore ('_') characters.")})

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name")
        labels = {
            'first_name': _('Given name'),
            'last_name': _('Family name (optional)'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control field-medium',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control field-medium',
                }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        if email == self.instance.email:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        if username == self.instance.username:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def save(self, commit=True):
        user = super(UserDetailsForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class GroupDetailsForm(forms.ModelForm):
    """
    A form that allows a user to edit their group details.
    """

    name = forms.CharField(label=_("Group name"), max_length=100,
        widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   }),
        help_text=_("Required. 100 characters or fewer."))

    class Meta:
        model = Group
        fields = ('name', 'aim', 'focus', 'country', 'logo' )
        help_texts = {
            'aim': _('A short statement of your group\'s main aim '
                     '(100 characters max.)'),
            'focus': _('e.g. refugee rights, climate change '
                       '(40 characters max.)'),
            'country': _('Your main country of operation '
                         '(40 characters max.)'),
        }
        widgets = {
            'aim': forms.TextInput(attrs={
                'class': 'form-control',
                }),
            'focus': forms.TextInput(attrs={
                'class': 'form-control',
                }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                }),
        }
     
    
