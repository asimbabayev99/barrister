from django.contrib import admin
from home.models import(
    Event, EventCategory, News, Publication, 
    Comment , Task, Appointment, City , Contact,
    Email, EmailAccount, Attachment
) 
from django.contrib.admin import AdminSite , ModelAdmin
from django.shortcuts import HttpResponse


class EmailAdmin(ModelAdmin):
    list_display = ('sender','subject','folder','date')
    list_filter =('folder','date')




admin.site.register(Publication)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Task)
admin.site.register(Appointment)
admin.site.register(City)
admin.site.register(Contact)

admin.site.register(Email,EmailAdmin)
admin.site.register(EmailAccount)
admin.site.register(Attachment)



