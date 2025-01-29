from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError


class RegistrationUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

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
            raise ValidationError('Этот никнейм уже занят.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('Этот email уже занят.')
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput())