###########################################################################
#   Author: Luke Clarke
#   Contributors:
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################
 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('scan/', views.scan, name='scan'),
]