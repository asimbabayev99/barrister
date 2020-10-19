from django.contrib import admin
from django.urls import path, re_path
from documents.views import *

urlpatterns = [

    path('templates', temlates_view, name='documents-templates'),
    path('templates/<int:id>', single_template_view, name='single-document-single'),
    path('test', test_view, name='documents-test'),

] 


