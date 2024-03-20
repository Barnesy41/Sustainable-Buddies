###########################################################################
#   Author: Silas Turner
#   Contributors: Ollie Barnes
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.contrib import admin

from .models import UserDetail, Friend, Group, GroupUser
from tasks.models import GroupTask, UserTask


###########################################################################
#   This function is used by the admin interface to assign all users in
#   a group a given task when the admin user assigns the group a task
#
#   Author: Ollie Barnes
###########################################################################
class GroupTaskAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the object
        super().save_model(request, obj, form, change)
        
        # retrieve all required objects
        group = obj.group
        task = obj.task
        group_users = group.groupuser_set.all()

        # Iterate over each user in the group, assigning the group task to each of them
        for group_user in group_users:
            user = group_user.user_id
            
            # If a UserTask entry doesn't exist, create it. Otherwise, retrieve it
            user_task_exists = UserTask.objects.filter(user_id=user, task_id=task).exists()
            usertask_obj = None
            if not user_task_exists:
                usertask_obj = UserTask.objects.create(user_id=user, task_id=task)
            else:
                usertask_obj = UserTask.objects.get(user_id=user, task_id=task)
                
            #Set the task's completion status to False
            usertask_obj.completion_status = False
            usertask_obj.save()
            

# Register models in the admin panel
admin.site.register(UserDetail)
admin.site.register(Friend)
admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(GroupTask, GroupTaskAdmin)
