from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='barrister-clients'),
    path("client/<int:id>", client_documents , name = 'barrister-clients-documents'),

    #document download
    path('document/<str:path>',case_document_download,name='document-download')
]
