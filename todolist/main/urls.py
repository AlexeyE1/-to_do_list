from django.urls import path
from .views import TaskListView, TaskAddView, TaskRemoveView, SyncSessionTasksView


app_name='main'


urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('add/', TaskAddView.as_view(), name='add_task'),
    path('remove/<int:task_id>/', TaskRemoveView.as_view(), name='remove_task'),
    path('remove/session/<int:session_index>/', TaskRemoveView.as_view(), name='remove_session_task'),
    path('sync/', SyncSessionTasksView.as_view(), name='sync_tasks'),
]