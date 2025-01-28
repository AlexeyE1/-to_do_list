from django.urls import path
from .views import RegistrationView, LoginUserView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


app_name='users'


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='main:task_list'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    # path('profile/', ProfileUser.as_view(), name='profile'),
]