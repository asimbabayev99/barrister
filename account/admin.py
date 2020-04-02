from django.contrib import admin
<<<<<<< HEAD
from account.models import CustomUser, Role, Contact, Profile , Skill, JobCategory
=======
from account.models import *
>>>>>>> 61afe4dcda052f1de35c5add7f2b1be99ea63577
from django.contrib.auth.models import Permission
# Register your models here.

admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(CustomUser)
<<<<<<< HEAD
admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(JobCategory)
=======
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Award)
admin.site.register(EducationAndWorkExperience)
admin.site.register(JobCategory)
>>>>>>> 61afe4dcda052f1de35c5add7f2b1be99ea63577
