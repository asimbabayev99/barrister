from django.contrib import admin
from home.models import Event, EventCategory, News, Publication, Comment , Task, Appointment, City , Contact
from django.contrib.admin import AdminSite 
from django.shortcuts import HttpResponse

admin.site.register(Publication)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Task)
admin.site.register(Appointment)
admin.site.register(City)
admin.site.register(Contact)
