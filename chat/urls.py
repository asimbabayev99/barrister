from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('<int:user_id>', index, name='chat-index'),
    path('upload_file/<int:user_id>/', upload_file, name='chat-upload-file'),
]
