from django.urls import path
from .views import TaskListView, TaskAddView, TaskRemoveView, TaskChangeStatusView, SyncSessionTasksView


app_name='main'


urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('add/', TaskAddView.as_view(), name='add_task'),
    path('remove/<int:task_id>/', TaskRemoveView.as_view(), name='remove_task'),
    path('remove/session/<int:task_counter>/', TaskRemoveView.as_view(), name='remove_session_task'),
    path('change_status/<int:task_id>/', TaskChangeStatusView.as_view(), name='change_status'),
    path('change_status/session/<int:task_counter>/', TaskChangeStatusView.as_view(), name='change_status_session'),
    path('sync/', SyncSessionTasksView.as_view(), name='sync_tasks'),
]