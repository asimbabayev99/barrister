from django.contrib import admin
from django.urls import path
from home.views import *

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from barrister import settings

urlpatterns = [

    path('', index_view, name='home'),
    path('calendar/', calendar_view, name='calendar'),
    path('profile/<int:id>', single_view, name='single-view'),
    path('news-add/',news_add_view,name='news-add')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
