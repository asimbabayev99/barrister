"""barrister URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'skills', SkillView, basename="Skill")

urlpatterns = [
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    # path('api-auth/',ExampleViews.as_view()),
    path('api/', include(router.urls)),
    path('api-register/',UserRegistration.as_view({'post':'create'})),
    path('api/task/list',EventList.as_view()),
    path('api/task/create',EventCreate.as_view()),
    path('api/task/detail/<int:id>',EventDetail.as_view()),
    path("api/skills/<int:pk>", SkillAPIView.as_view()),
    path('api/skills/', SkillAPIView.as_view()),
    path('api/awards/<int:pk>', AwardAPIView.as_view()),
    path('api/awards/', AwardAPIView.as_view()),   
    path('api/experiences/<int:pk>', ExperienceAPIView.as_view()),
    path('api/experiences/', ExperienceAPIView.as_view()),

]
