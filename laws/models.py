from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Code(models.Model):
    name = models.CharField(max_length=128)
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    content = RichTextField()



# class Division(models.Model):
#     name = models.CharField(max_length=256)
#     number = models.IntegerField(default=1)
#     code = models.ForeignKey(Code, related_name='divisions', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.number + "." + self.name

#     class Meta:
#         indexes = [
#             models.Index(fields=['code', 'name']),
#             models.Index(fields=['code', 'number']),
#         ]


# class Section(models.Model):
#     name = models.CharField(max_length=256)
#     number = models.IntegerField(default=1)
#     division = models.ForeignKey(Division, related_name='sections', on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.number) + "." + self.name

#     class Meta:
#         indexes = [
#             models.Index(fields=['division', 'name']),
#         ] 
