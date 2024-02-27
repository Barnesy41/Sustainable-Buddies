###########################################################################
#   Author: Luke Clarke
#   Contributors: Ollie Barnes
#
#   The author has written all code in this file unless stated otherwise.
###########################################################################

from django.db import models
from users.models import UserDetail
from users.models import User

class Task(models.Model):
    TaskName = models.CharField(max_length=200)
    Description = models.CharField(max_length=400)
    DifficultyLevel = models.CharField(max_length=10)
    CoinReward = models.IntegerField(default=0)
    XpReward = models.IntegerField(default=0)

    def __str__(self):
        return self.TaskName

# The below was written by Ollie Barnes #
class UserTask(models.Model):
    completion_status = models.IntegerField(default=0)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)