from django.db import models
from account.models import CustomUser
# Create your models here.


CLIENT_STATUSES = [
    ('active', 'Aktiv'),
    ('inactive', 'Aktiv deyil')
]

class Client(models.Model):
    barrister = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=16)
    status = models.CharField(max_length=16, choices=CLIENT_STATUSES, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['barrister', 'name', 'email']),
        ]




class Case(models.Model):
    barrister = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=64, default="unnamed")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['barrister', 'name']),
        ]



class CaseDocument(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=64)
    document = models.TextField(null=False, blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['case', 'name']),
        ]
 

