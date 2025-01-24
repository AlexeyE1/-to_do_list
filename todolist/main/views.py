from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View
from .tasks import ToDoList
from .models import Task


# Create your views here.

class HomeView(TemplateView):
    template_name = 'main/home.html'


class AddTaskView(View):
    def post(self, request):
        #task_text = request.POST.get('task', '').strip()
        