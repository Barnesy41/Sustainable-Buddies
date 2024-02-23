from django.urls import path
from . import views

urlpatterns = [
    # ex: /tasks/5/
    path("<int:task_id>/", views.detail, name="detail"),
    path('', views.task_list, name='tasks'),
]