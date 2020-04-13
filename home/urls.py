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
    path('news-add/',news_add_view,name='news-add'),
    path('news-update/<slug:slug>',news_update,name='news-update'),
    path('news/',news_view,name='news'),
    path('news/<slug:slug>', news_detail_view, name='news_detail'),
    path('about-us/',about_us_view,name='contacts'),
  
    path('admin/user/list', admin_user_list, name='admin-user-list'),
    path('admin/home/news/add_news',admin_add_news,name='admin-add-news')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
