###########################################################################
#   Author: Silas Turner
#   Contributors: Ollie Barnes
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.contrib import admin
from .models import Task, UserTask, GroupTask


###########################################################################
#   This function is used by the admin interface to assign a user a task.
#   It ensures that the user cannot be assigned the same task more than once.
#   It does this by setting the task status to incomplete if already assigned
#   to them. Otherwise, it assigns the task to them.
#
#   Author: Ollie Barnes
###########################################################################
class UserTaskAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):

        # retrieve all required objects
        task = obj.task_id
        user = obj.user_id
        
        # If a UserTask entry doesn't exist, create it. Otherwise, retrieve it
        user_task_exists = UserTask.objects.filter(user_id=user, task_id=task).exists()
        user_task_obj = None
        if not user_task_exists:
            user_task_obj = UserTask.objects.create(user_id=user, task_id=task)
        else:
            user_task_obj = UserTask.objects.get(user_id=user, task_id=task)
            
        #Set the task's completion status to False
        user_task_obj.completion_status = False
        user_task_obj.save()
            
            
# Register models in the admin panel
admin.site.register(Task)
admin.site.register(UserTask, UserTaskAdmin)