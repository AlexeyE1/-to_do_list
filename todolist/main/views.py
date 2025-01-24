from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View
from .models import Task
from django.shortcuts import redirect


class TaskListView(View):
    def get(self, request):
        session_tasks = request.session.get('tasks', [])
        
        db_tasks = Task.objects.filter(user=request.user) if request.user.is_authenticated else []

        return render(request, 'main/home.html', {
            'session_tasks': session_tasks,
            'db_tasks': db_tasks
        })


class TaskAddView(View):
    def post(self, request):
        task_text = request.POST.get('task', '').strip()
        if task_text:
            if request.user.is_authenticated:
                Task.objects.create(user=request.user, text=task_text)
            else:
                session_tasks = request.session.get('tasks', [])
                session_tasks.append({'text': task_text, 'completed': False})
                request.session['tasks'] = session_tasks
        print(request.session['tasks'])
        return redirect('main:task_list')
       


class TaskRemoveView(View):
    def post(self, request, task_id=None, session_index=None):
        if request.user.is_authenticated and task_id:
            Task.objects.filter(id=task_id, user=request.user).delete()
        elif session_index is not None:
            session_tasks = request.session.get('tasks', [])
            if 0 <= session_index < len(session_tasks):
                session_tasks.pop(session_index)
                request.session['tasks'] = session_tasks
        return redirect('main:task_list')


class SyncSessionTasksView(View):
    def post(self, request):
        if request.user.is_authenticated:
            session_tasks = request.session.get('tasks', [])
            for session_task in session_tasks:
                Task.objects.create(
                    user=request.user,
                    text=session_task['text'],
                    completed=session_task['completed']
                )
            request.session['tasks'] = []
        return redirect('main:task_list')