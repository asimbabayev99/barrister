from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Code)
admin.site.register(LawType)
admin.site.register(LawAgency)
admin.site.register(Law)
admin.site.register(Division)
admin.site.register(Chapter)
admin.site.register(Matter)