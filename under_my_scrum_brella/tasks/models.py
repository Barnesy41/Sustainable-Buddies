from django.db import models
from users.models import UserDetail

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
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)