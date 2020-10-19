from django.contrib import admin
from django.urls import path, re_path
from documents.views import *

urlpatterns = [

    path('index', index_view, name='docuemtns-index'),
    path('test', test_view, name='documents-test'),

] 


