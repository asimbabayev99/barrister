from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class LawType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name',]),
        ]


class LawAgency(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name',])
        ]


class Code(models.Model):
    name = models.CharField(max_length=128)
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    content = RichTextField()



class Law(models.Model):
    name = models.CharField(max_length=128)
    number = models.IntegerField()
    active = models.BooleanField(default=True)
    type = models.ForeignKey(LawAgency, on_delete=models.DO_NOTHING)
    header = RichTextField()
    content = RichTextField()
    footer = RichTextField()



class Division(models.Model):
    name = models.CharField(max_length=256)
    number = models.IntegerField(default=1)
    law = models.ForeignKey(Law, related_name='divisions', on_delete=models.CASCADE)

    def __str__(self):
        return self.number + "." + self.name

    class Meta:
        indexes = [
            models.Index(fields=['law', 'name']),
            models.Index(fields=['law', 'number']),
        ]


class Chapter(models.Model):
    name = models.CharField(max_length=256)
    number = models.IntegerField(default=1)
    division = models.ForeignKey(Division, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number) + "." + self.name

    class Meta:
        indexes = [
            models.Index(fields=['division', 'name']),
        ] 


class Matter(models.Model):
    name = models.CharField(max_length=256)
    number = models.IntegerField()
    chapter = models.ForeignKey(Chapter, related_name='chapters', on_delete=models.CASCADE)
    content = RichTextField()

    def __str__(self):
        return str(self.number) + "." + self.name

    class Meta:
        indexes = [
            models.Index(fields=['chapter', 'name']),
        ]
