from django.contrib import admin
from django.urls import path, re_path
from .views import *

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from barrister import settings

urlpatterns = [

    path('index', index, name='laws-index'),
    path('codes', codes, name='laws-codes'),
    path('code/<int:id>', code_single, name='laws-code-single'),

]


