from django.contrib import admin
from django.urls import path, include 
from api.views import *
from rest_framework import routers



urlpatterns = [
    
    path('auth/',LoginView.as_view()),
    path('user/<int:pk>', UserAPI.as_view()),
    path('register/',UserRegistration.as_view()),
    
    path('news/list/',NewsList.as_view()),
    path('news/create/',NewsAPI.as_view()),
    path('news/detail/<int:pk>',NewsAPI.as_view()),

    path('task/list',TaskList.as_view()),
    path('task/detail/<int:pk>',TaskDetail.as_view()),
    path('task/create',TaskDetail.as_view()),

    path('product/list/',ProductList.as_view()),

    path('basket/list/',BasketList.as_view()),
    path('basket/add',BasketDetail.as_view()),
    path('basket/delete/<int:pk>',BasketDetail.as_view()),
    path('basket/<int:pk>',BasketDetail.as_view()),

    path('profile/list/',ProfilesList.as_view()),
    path('profile/<int:id>',ProfileDetail.as_view()),
    path('profile/create',ProfileCreate.as_view()), 

    path("skills/<int:pk>", SkillAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),

    path('awards/<int:pk>', AwardAPIView.as_view()),
    path('awards/', AwardAPIView.as_view()),   

    path('experiences/<int:pk>', ExperienceAPIView.as_view()),
    path('experiences/', ExperienceAPIView.as_view()),

    path('publication/',PublicationAPIView.as_view()),
    path('publication/list',PublicationListView.as_view()),
    path('publication/<int:pk>',PublicationAPIView.as_view()),

    path('emails/', EmailList.as_view()),
    path('emails/trash/list/',EmailTrashList.as_view()),
    path('email/move/folder/',EmailFolderMove.as_view()),
    path('email/delete/',EmailDeleteView.as_view()),
    path('email/change/flag',EmailChangeFlag.as_view()),

    path('events/list/', EventListView.as_view()),
    path('events/', EventAPIView.as_view()),
    path('events/<int:id>/', EventAPIView.as_view()),

    path('appointments/list/', AppointmentListView.as_view()),
    path('appointments/', AppointmentAPIView.as_view()),
    path('appointments/<int:id>/', AppointmentAPIView.as_view()),

]