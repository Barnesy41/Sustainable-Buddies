from django.shortcuts import render, get_object_or_404
from .models import Task
from users.models import UserDetail
    
def task_list(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    user = request.user
    if user.is_authenticated:
        user_details = get_object_or_404(UserDetail, pk=user.id)
        context['user_details'] = user_details
        return render(request, 'tasks.html', context)
    else:
        return render(request, 'tasks.html', context)