###########################################################################
#   Author: Ollie Barnes
#   Contributors: Luke Clarke, Silas Turner
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################
 
 
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task, UserTask
from users.models import UserDetail
from django.contrib.auth import authenticate
from django.contrib import messages


###########################################################################
#   This function is used to render the tasks.html page, 
#   and provide tasks.html with the required information from the database
###########################################################################
def task_list(request):
    #Redirect the user if not authenticated
    current_user = request.user
    if not current_user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')
    
    #Redirect the user if they're the admin account type
    if current_user.is_superuser:
        return redirect('/admin/')
    
    #If authenticated, render the tasks.html web page with the required data
    if request.method == 'POST':
        task_id = request.POST["task_id"]
        
        #Update the completion status of the user's recently completed task from 0 (incomplete) to 1 (complete)
        task_object = UserTask.objects.get(task_id=task_id, user_id=current_user)
        task_object.completion_status = 1
        task_object.save()
        
        #Add coins & XP to the user's account
        user = UserDetail.objects.get(user=current_user)    
        task_object = Task.objects.get(id=task_id)

        user.total_coins = user.total_coins + task_object.CoinReward
        user.total_xp = user.total_xp + task_object.XpReward
        user.save()
        
        return redirect('tasks')
    
    # Written by Luke Clarke
    #Get the list of all tasks
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    #Written by Luke Clarke End
    
    #Get all tasks assigned to the given user
    assigned_tasks = UserTask.objects.filter(user_id=current_user)
    context['assigned_tasks'] = assigned_tasks
    
    #Get the details for the current user
    user_details = get_object_or_404(UserDetail, pk=current_user.id)
    context['user_details'] = user_details
    
    return render(request, 'tasks.html', context)