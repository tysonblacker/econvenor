import hashlib

from django import forms

from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from accounts.models import Group


class UserRegisterForm(forms.ModelForm):
    """
    A form that creates a user. Assigns a SHA1 hash of email address as a
    temporary username.This is a modified version of Django's UserCreationForm.
    """
    error_messages = {
        'duplicate_email': _("A user with that email address already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(label=_("Email"),
        error_messages={
            'invalid': _("This must be a valid email address.")})
    password1 = forms.RegexField(label=_("Password"), min_length=8,
        regex=r'[(?=.\d)]',
        widget=forms.PasswordInput,
        error_messages={
            'invalid': _("Passwords must be at least 8 characters long and "
                         "include at least 1 digit.")})
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput)
    username = forms.CharField(initial="PlaceholderText",
                               widget=forms.HiddenInput)
    
    class Meta:
        model = User
        fields = ("email", "username",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def clean_username(self):
        password = self.data["email"]
        password_hash = hashlib.sha1(password).hexdigest()
        username = password_hash[:30]
        return username
            
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

       
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
