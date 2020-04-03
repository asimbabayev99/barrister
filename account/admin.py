from django.contrib import admin
from account.models import CustomUser, Role,  Profile , Skill, JobCategory
from account.models import *
from django.contrib.auth.models import Permission
# Register your models here.

admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(CustomUser)

admin.site.register(Profile)
admin.site.register(Skill)



admin.site.register(Award)
admin.site.register(EducationAndWorkExperience)
admin.site.register(JobCategory)
