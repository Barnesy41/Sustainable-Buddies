###########################################################################
#   Author: Silas Turner
#   Contributors:
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.contrib import admin

from .models import UserDetail, Friend, Group, GroupUser

admin.site.register(UserDetail)
admin.site.register(Friend)
admin.site.register(Group)
admin.site.register(GroupUser)