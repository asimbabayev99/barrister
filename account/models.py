from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission
# Create your models here.



CONTACT_TYPES = [
    ('e-mail', 'e-mail'),
    ('phone', 'phone')
]


GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
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




class JobCategory(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()



class Skill(models.Model):
    name = models.CharField(max_length=32)
    progress = models.IntegerField(default=100)  # for example 70/100


class EducationAndWorkExperience(models.Model):
    title = models.CharField(max_length=256)
    from_time = models.DateField(auto_now_add=True)
    to_time = models.DateField(null=True)


class Award(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    # contacts
    phone_number = models.BigIntegerField(null=True)
    website = models.URLField(null=True)
    address = models.CharField(max_length=256, null=True)

    gender = models.CharField(max_length=32, choices=GENDER_CHOICES)
    skills = models.ManyToManyField(Skill)
    experiences = models.ManyToManyField(EducationAndWorkExperience)
    awards = models.ManyToManyField(Award)
    biography = models.TextField()
    job_category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.email

