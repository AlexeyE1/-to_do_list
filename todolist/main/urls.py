from django.urls import path
from . import views


app_name='main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # http://127.0.0.1:8000
]
