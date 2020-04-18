from django.contrib import admin
from django.urls import path, include
from account.views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('users/list/', user_list_view, name='user-list'),
    path('profile/', user_profile, name='user-profile'),
]
