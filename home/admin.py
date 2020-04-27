from django.contrib import admin
from home.models import Event, EventCategory, News, Publication, Comment , Task
from django.contrib.admin import AdminSite 
from django.shortcuts import HttpResponse

admin.site.register(Publication)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Task)
