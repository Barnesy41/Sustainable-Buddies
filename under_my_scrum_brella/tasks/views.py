from django.shortcuts import render, get_object_or_404
from .models import Task

#this is just for testing purposes, can remove later
#TODO: More thorough error catching
def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "detail.html", {"task": task})
    
def task_list(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'tasks.html', context)


