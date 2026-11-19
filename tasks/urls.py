from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.task_list, name='list'),
    path('tasks/new/', views.task_create, name='create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='delete'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle, name='toggle'),
]