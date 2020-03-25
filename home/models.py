from django.db import models

# Create your models here.


class TaskCategory(models.Model):
    name = models.CharField(max_length=64)


class Task(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    location = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)

    # all_day = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    from_time = models.TimeField(auto_now=True)
    to_time = models.TimeField(auto_now=True)

    remind_me = models.DateTimeField(auto_now=True)
