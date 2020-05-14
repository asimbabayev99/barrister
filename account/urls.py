from django.contrib import admin
from django.urls import path, include
from account.views import *
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView , PasswordResetCompleteView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('change-password', change_password, name='change-password'),
    path('password-reset/',PasswordResetView.as_view(template_name='account/password-reset.html')),
    path('password-reset/done',PasswordResetDoneView.as_view(template_name="account/password-reset-done.html"),name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>',PasswordResetConfirmView.as_view(template_name="account/password-reset-confirm.html"),name="password_reset_confirm"), 
    path('password-reset/complete',PasswordResetCompleteView.as_view(template_name="account/password-reset-complate.html"),name="password_reset_complete"),
    
    # barrister related
    path('clients/', barrister_clients, name='barrister-clients'),
    path('social-activity/', barrister_social_activity, name='barrister-social-activity'),
    path('users/list/', user_list_view, name='user-list'),
    path('add-contact/', add_contact, name='add-contact'),
    path('contact-list/', contact_list, name='contact-list'),

    # user related
    path('profile/', user_profile, name='user-profile'),
]
