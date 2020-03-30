from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission
# Create your models here.



CONTACT_TYPES = [
    ('e-mail', 'e-mail'),
    ('phone', 'phone')
]


GENDER_CHOICES = [
    ('male', 'male'),
    ('female', 'female')
]


class Role(models.Model):
    name = models.CharField(max_length=32)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name



class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = CustomUser(email = email, is_staff=is_staff,
                    is_superuser=is_superuser, date_joined=now,
                    **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
    


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    username = models.CharField('username', max_length=150, unique=False)
    email = models.EmailField(max_length=256, unique=True)

    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    def get_permission(self):
        permission = Permissions.objects.get(user=self.id)
      
        return permission.permission




class Contact(models.Model):
    type = models.CharField(max_length=32, choices=CONTACT_TYPES)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField()
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES)
    contacts = models.ManyToManyField(Contact)
    biography = models.TextField()

