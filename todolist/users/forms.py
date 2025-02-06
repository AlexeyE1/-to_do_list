from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox 


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=63, widget=forms.TextInput())
    email = forms.EmailField(label='Email', max_length=255, help_text='Required field. Enter a valid email.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'captcha')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ProfileUserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError('This nickname is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('This email is already taken')
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Previous Password", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Confirm Password",
                                    widget=forms.PasswordInput())