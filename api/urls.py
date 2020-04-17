from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'skills', SkillView, basename="Skill")


urlpatterns = [

    path('auth/',LoginView.as_view()),
    path('register/',UserRegistration.as_view()),
    path('event/list',EventList.as_view()),
    path('event/create',EventCreate.as_view()),
    path('event/detail/<int:id>',EventDetail.as_view()),
    path('profile/list/',ProfilesList.as_view()),
    path('profile/<int:id>',ProfileDetail.as_view()),
    path('profile/create',ProfileCreate.as_view()),
    path('', include(router.urls)),
    path("skills/<int:pk>", SkillAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('awards/<int:pk>', AwardAPIView.as_view()),
    path('awards/', AwardAPIView.as_view()),   
    path('experiences/<int:pk>', ExperienceAPIView.as_view()),
    path('experiences/', ExperienceAPIView.as_view()),

]