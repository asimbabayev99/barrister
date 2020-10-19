from django.db import models

# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    template = models.FileField(upload_to='documents', null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
