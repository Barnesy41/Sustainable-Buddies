###########################################################################
#   Author: Ollie Barnes
#   Contributors: Luke Clarke, Silas Turner, Jack Bundy
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################
 
 
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task, UserTask
from users.models import UserDetail
from django.contrib.auth import authenticate
from django.contrib import messages

from math import sqrt


###########################################################################
#   This function is used to render the tasks.html page, 
#   and provide tasks.html with the required information from the database
###########################################################################
def task_list(request):
    #How much happiness increases upon task completion
    taskHappiness = 0.1

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
        
        #Add coins, XP and happiness to the user's account
        user = UserDetail.objects.get(user=current_user)    
        task_object = Task.objects.get(id=task_id)

        user.total_coins = user.total_coins + task_object.CoinReward
        user.total_xp = user.total_xp + task_object.XpReward

        #Luke Clarke - Sets buddy happiness (between 0 and 1)
        newHappiness = max(0, min(1, user.buddy_happiness + taskHappiness))
        user.buddy_happiness = newHappiness

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

# QR done by Jack Bundy
def scan(request): 
    if not request.user.is_authenticated:
        messages.success(request, "Please login first")
        return redirect('login')

    if request.method == "POST": 
        print(request.POST)
        task_hash = request.POST["QR-val"]
        task_lat = float(request.POST["Geo-lat"])
        task_long = float(request.POST["Geo-long"])

        # Find the task, see if can be completed, add task to user, complete task
        task_object = Task.objects.get(QrData=task_hash)
        
        if sqrt((task_object.GeoLat-task_lat)**2 + (task_object.GeoLong-task_long)**2) <= task_object.GeoRange:
            print("Inside range")
            print(sqrt((task_object.GeoLat-task_lat)**2 + (task_object.GeoLong-task_long)**2))
        else:
            messages.success(request, "You are not close enough to the task to complete it!")

        return redirect('tasks')


    context = {}
    return render(request, 'scan.html', context)