from django.shortcuts import redirect
from users.forms import LoginUserForm, RegistrationUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.mail import send_mail
from django.urls import reverse


class RegistrationView(CreateView):
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


class ProfileUserView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileUserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:profile'))
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


# class EmailChangeRequestView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         confirmation_url = request.build_absolute_uri(
#                 reverse('confirm_email_change', args=[change_request.confirmation_key])
#             )