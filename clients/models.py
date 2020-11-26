from django.db import models
from account.models import CustomUser
# Create your models here.


CLIENT_STATUSES = [
    ('active', 'Aktiv'),
    ('inactive', 'Aktiv deyil')
]

CASE_STATUSES = [
    ('Bağlı','Bağlı'),
    ('Uğurlu',"Uğurlu"),
    ('Davam edir','Davam edir')
]



class Client(models.Model):
    barrister = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False,related_name='clients')
    first_name = models.CharField(max_length=64,blank=True,null=True)
    last_name = models.CharField(max_length=64,blank=True,null=True)
    image = models.ImageField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=16)
    status = models.CharField(max_length=16, choices=CLIENT_STATUSES, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.email
    
    class Meta:
        indexes = [
            models.Index(fields=['barrister','email']),
        ]
    def is_user(self):
        return CustomUser.objects.filter(first_name=self.first_name,last_name=self.last_name,email=self.email).exists()
    
    def get_user_id(self):
        return self.user.id

class Case(models.Model):
    barrister = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=64, default="unnamed")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False,related_name='case')
    status = models.CharField(max_length=30,choices=CASE_STATUSES,default="Bağlı")
    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['barrister', 'name']),
        ]



class CaseDocument(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=False, blank=False,related_name='documents')
    name = models.CharField(max_length=64)
    document = models.FileField(upload_to='case-documents')

    class Meta:
        indexes = [
            models.Index(fields=['case', 'name']),
        ]
    # @property
    def download_url(self):
        return '/clients/document'+self.document.url
 

class Notes(models.Model):
    text = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['date'])
        ]