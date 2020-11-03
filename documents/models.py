from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.



class DocumentGroup(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)

    def __str__(self):
        return self.name



class Document(models.Model):
    group = models.ForeignKey(DocumentGroup, related_name='documents', on_delete=models.SET_NULL, null=True)

    # name and content
    name = models.CharField(max_length=128, null=False, blank=False)
    content = models.TextField()

    # html and js for form fill
    form_html = models.TextField()
    form_js = models.TextField()

    # json configuration to build dynamically
    conf = JSONField()

    # created date
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
