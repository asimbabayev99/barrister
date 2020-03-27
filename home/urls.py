from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('', calendar_view, name='home'),
    path('calendar/', calendar_view, name='calendar'),
]
