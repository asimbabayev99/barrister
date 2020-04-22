from django.contrib import admin
from django.urls import path
from shop.views import *

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from barrister import settings

urlpatterns = [
    
    path('', shop_view, name='shop'),
    path('<str:category>/', shop_view, name='shop'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
