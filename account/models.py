from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission
from django.utils import timezone



GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
]


SERIYA_TYPES = [
    ('AZE', 'AZE'),
    ('AA', 'AA')
]


PHONE_PREFIXES = [
    ('050', '050'),
    ('051', '051'),
    ('055', '055'),
    ('070', '070'),
    ('077', '077')
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
    middle_name = models.CharField(max_length=100,unique=False, null=True)
    username = models.CharField('username', max_length=150, unique=False)
    email = models.EmailField(max_length=256, unique=True)
    fin = models.CharField(max_length=10, unique=True, null=True)
    seriya_type = models.CharField(max_length=3, choices=SERIYA_TYPES)
    seriya = models.IntegerField(unique=True, null=True)
    phone_prefix = models.CharField(max_length=4, choices=PHONE_PREFIXES, null=True)
    phone_number = models.IntegerField(null=True)

    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    




class JobCategory(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    def __str__(self):
        return self.name




class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    # contacts
    phone_number = models.BigIntegerField(null=True)
    website = models.URLField(null=True)
    address = models.CharField(max_length=256, null=True)

    # social networks
    facebook_link = models.URLField(null=True)
    twitter_link = models.URLField(null=True)
    linkedin_link = models.URLField(null=True)
    google_link = models.URLField(null=True)

    gender = models.CharField(max_length=32, choices=GENDER_CHOICES)
    work_summary = models.CharField(max_length=2014)
    biography = models.TextField()
    job_category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)    




class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=32)
    progress = models.IntegerField(default=100)  # for example 70/100



class EducationAndWorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=256)
    start = models.DateField(auto_now_add=True)
    end = models.DateField(null=True)



class Award(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)