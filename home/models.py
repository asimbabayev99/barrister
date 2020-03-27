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


class Event(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    location = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=32, choices=FREQUENCY_TYPES)
    frequency_count = models.IntegerField(default=1)
    date = models.DateField(auto_now=True)
    from_time = models.TimeField(auto_now=True)
    to_time = models.TimeField(auto_now=True)

    remind_me = models.DateTimeField(auto_now=True)
