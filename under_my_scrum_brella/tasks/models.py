from django.db import models


class Task(models.Model):
    TaskName = models.CharField(max_length=200)
    Description = models.CharField(max_length=400)
    DifficultyLevel = models.CharField(max_length=10)
    CoinReward = models.IntegerField(default=0)
    XpReward = models.IntegerField(default=0)

    def __str__(self):
        return self.TaskName
