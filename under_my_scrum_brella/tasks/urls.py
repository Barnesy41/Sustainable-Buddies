from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('task-complete/', views.task_complete, name='task_complete')
]