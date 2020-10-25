from django.db import models
from account.models import CustomUser
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender_messages', null=False, blank=False)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver_messages', null=False, blank=False)
    text = models.TextField()
    viewed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'date']),
            models.Index(fields=['receiver', 'date']),
        ]


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message',]),
        ]