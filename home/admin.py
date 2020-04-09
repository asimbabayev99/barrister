from django.contrib import admin
from home.models import Event, EventCategory, News, Publication

admin.site.register(Publication)
admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(News)