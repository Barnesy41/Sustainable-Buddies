from django.shortcuts import redirect, render, get_object_or_404
from .models import Task, UserTask
from users.models import UserDetail
from django.contrib.auth import authenticate
from django.contrib import messages

# This is a list of all tasks, NOT a specific user's tasks  #
# if you want a user's tasks, please use user_tasks instead #
def task_list(request):
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    if request.method == 'POST':
        task_id = request.POST["task_id"]
        
        #Update the completion status of the task
        task_object = UserTask.objects.get(task_id=task_id)
        task_object.completion_status = 1     #update the completion status from 0 (incomplete) to 1 (complete)
        task_object.save()
        
        #Add coins & XP to the user's account
        user = UserDetail.objects.get(user=request.user)    
        task_object = Task.objects.get(id=task_id)

        user.total_coins = user.total_coins + task_object.CoinReward
        user.total_xp = user.total_xp + task_object.XpReward
        user.save()
        return redirect('tasks')
    
    user = request.user
    
    #Get the list of all tasks
    #TODO: currently redundant
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    
    #Get all tasks assigned to the given user
    assigned_tasks = UserTask.objects.filter(user_id=user)
    context['assigned_tasks'] = assigned_tasks
    
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context['user_details'] = user_details
        return render(request, 'tasks.html', context)
    else:
        return render(request, 'tasks.html', context)