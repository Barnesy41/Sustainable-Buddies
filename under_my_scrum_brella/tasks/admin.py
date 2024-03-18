###########################################################################
#   Author: Silas Turner
#   Contributors: Ollie Barnes
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.contrib import admin
from .models import Task, UserTask, GroupTask

admin.site.register(Task)
admin.site.register(UserTask)
admin.site.register(GroupTask)
