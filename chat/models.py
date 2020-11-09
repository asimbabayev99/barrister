from django.db import models
from account.models import CustomUser
import uuid
import os
from django.conf import settings
from account.models import CustomUser
# Create your models here.



class Channel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return self.channel_name



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



def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid1(), ext)
    return 'chat/attachments/' + filename
    # return os.path.join(settings.MEDIA_ROOT, 'chat', 'attachments', filename)


class Attachment(models.Model):
    message = models.OneToOneField(Message, related_name='attachment', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to=path_and_rename, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message',]),
        ]