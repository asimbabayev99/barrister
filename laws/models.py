from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Code(models.Model):
    name = models.CharField(max_length=128)
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    content = RichTextField()