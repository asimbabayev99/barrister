from django.contrib import admin
from clients.models import *
# Register your models here.

admin.site.register(Client)
admin.site.register(Case)
admin.site.register(CaseDocument)
admin.site.register(Notes)