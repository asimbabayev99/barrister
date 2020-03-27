from django.contrib import admin
from home.models import Task,TaskCategory

admin.site.register(Task)
admin.site.register(TaskCategory)