from django.shortcuts import redirect
from users.forms import LoginUserForm, RegistrationUserForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate


class RegistrationView(CreateView):
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'