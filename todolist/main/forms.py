from django import forms
from .models import Task


class AddTaskView(forms.ModelForm):
    class Meta:
        model = Task
        