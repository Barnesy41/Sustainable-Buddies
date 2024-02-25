from django.shortcuts import render, get_object_or_404
from .models import Task, UserTask
from users.models import UserDetail
    
# This is a list of all tasks, NOT a specific user's tasks  #
# if you want a user's tasks, please use user_tasks instead #
def task_list(request):
    user = request.user
    
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    
    assigned_tasks = UserTask.objects.filter(user_id=user)
    context['assigned_tasks'] = assigned_tasks
    
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context['user_details'] = user_details
        return render(request, 'tasks.html', context)
    else:
        return render(request, 'tasks.html', context)
