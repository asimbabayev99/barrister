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
    path('news/',news_view,name='news'),
    path('news/<slug:slug>', news_detail_view, name='news_detail'),
    path('about-us/',about_us_view,name='contacts'),
    
    path('blog/', blog_grid_view, name='blog'),
  
    path('admin/user/list', admin_user_list, name='admin-user-list'),
    path('admin/news/add_news',admin_add_news,name='admin-add-news'),
    path('admin/news/list',admin_news_list,name='admin-news-list'),
    path('admin/news/update/<slug:slug>',admin_news_update,name='admin-news-update'),
    path('admin/user/add', admin_user_add, name='admin-user-add'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
