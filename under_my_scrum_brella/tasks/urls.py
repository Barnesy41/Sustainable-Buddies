from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('complete-task/', views.task_complete, name='complete-task')
]