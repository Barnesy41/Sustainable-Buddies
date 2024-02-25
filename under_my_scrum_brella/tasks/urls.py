from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('tasks/', views.task_complete, name='tasks')
]