from django.contrib import admin
from chat.models import *

# Register your models here.
admin.site.register(Message)
admin.site.register(Attachment)
admin.site.register(Channel)