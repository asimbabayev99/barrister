from django.contrib import admin
from django.urls import path, re_path
from home.views import *

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from barrister import settings

urlpatterns = [

    path('', index_view, name='home'),
    path('calendar/', calendar_view, name='calendar'),
    path('barrister/<int:id>', single_view, name='single-view'),
    path('about-us/', about_us_view, name='about-us'),

    path('publication/add', publication_add_view, name='publication-add'),
    
    path('blog-grid/', blog_grid_view, name='blog-grid'),
    path('blog-large/',blog_large_view,name='blog-large'),
    path('blog-single/',blog_single_view,name='blog-single'),

    path('admin/user/list', admin_user_list, name='admin-user-list'),
    path('admin/user/add', admin_user_add, name='admin-user-add'),
    path('admin/news/add', admin_add_news, name='admin-add-news'),
    path('admin/news/list', admin_news_list, name='admin-news-list'),
    path('admin/news/update/<slug:slug>', admin_news_update, name='admin-news-update'),
    path('contacts/',contacts_view,name='contacts'),
    path('attorneys/', attorneys_view, name='attorneys'),

    path('is-masasi/',is_masasi,name='is-masasi'),
    path('barrister/dashboard/', is_masasi, name='barrister-dashboard'),
    path('barrister/account/', barrister_account, name='barrister-account'),
    path('barrister/new-appointment/', new_appointment_view, name='barrister-new-appointment'),
    path('barrister/new-task/', add_task_view, name='barrister-add-task'),
    path('barrister/completed-tasks/', barrister_completed_tasks, name='barrister-completed-tasks'),
    path('barrister/current-tasks/', barrister_current_tasks, name='barrister-current-tasks'),
    path('barrister/personal', barrister_personal, name='barrister-personal'),
    path('barrister/skills', barrister_professional_skills, name='barrister-skills'),

    path('email/send', send_email, name='send-email'),
    path('email/', email_view, name='email'),


    re_path(r'^media/attachment/(?P<path>.*)', attachment_media_access, name='atatchment-media'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


