from django.db import models
from account.models import CustomUser
# Create your models here.


FREQUENCY_TYPES = [
    ('Fixed', 'fixed'),
    ('Daily', 'daily'),
    ('Weekly', 'weekly'),
    ('Monthly', 'monthly'),
    ('Yearly', 'yearly')
]


class EventCategory(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    location = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_all_day = models.BooleanField(default=False)
    from_time = models.DateTimeField(auto_now_add=True)
    to_time = models.DateTimeField(auto_now_add=True)

    remind_me = models.DateTimeField(auto_now_add=True)
