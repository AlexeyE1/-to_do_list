from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View
from .models import Task
from django.shortcuts import redirect
from django.db.models import F
import datetime


class TaskListView(View):
    def get(self, request):

        session_tasks = request.session.get('tasks', [])
        
        db_tasks = Task.objects.filter(user=request.user).order_by('completed', '-id') if request.user.is_authenticated else []
        print(db_tasks)
        return render(request, 'main/home.html', {
            'session_tasks': sorted(session_tasks, key=lambda x: (not(x['completed']), x['task_counter']), reverse=True),
            'db_tasks': db_tasks,
            'is_authenticated': request.user.is_authenticated,
        })


class TaskAddView(View):
    def post(self, request):
        task_text = request.POST.get('task', '').strip()
        if task_text:
            if request.user.is_authenticated:
                Task.objects.create(user=request.user, text=task_text)
            else:
                if 'task_counter' not in request.session:
                    request.session['task_counter'] = 0

                session_tasks = request.session.get('tasks', [])
                session_tasks.append({'text': task_text, 'completed': False, 'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      'task_counter':  request.session['task_counter']})
                request.session['tasks'] = session_tasks
                request.session['task_counter'] += 1
        return redirect('main:task_list')
       


class TaskRemoveView(View):
    def post(self, request, task_id=None, task_counter=None):
        if request.user.is_authenticated and task_id:
            Task.objects.filter(id=task_id, user=request.user).delete()
        elif task_counter is not None:
            session_tasks = request.session.get('tasks', [])
            request.session['tasks'] = [task for task in session_tasks if task['task_counter'] != task_counter]
        return redirect('main:task_list')


class TaskChangeStatusView(View):
    def post(self, request, task_id=None, task_counter=None):
        print(request.user.is_authenticated)
        if request.user.is_authenticated and task_id:
            tasks = Task.objects.filter(id=task_id, user=request.user)
            tasks.update(completed=~F('completed'))
        elif task_counter is not None:
            session_tasks = request.session.get('tasks', [])
            for task in session_tasks:
                if task['task_counter'] == task_counter:
                    task['completed'] = not(task['completed'])
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
                    completed=session_task['completed'],
                )
            request.session['tasks'] = []
        return redirect('main:task_list')
    
    def get(self, request):
        return render(request, 'main/sync_tasks.html')