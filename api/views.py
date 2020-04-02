from django.shortcuts import render
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.generics import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication , BasicAuthentication , BaseAuthentication
from django.views.decorators.csrf import  csrf_exempt,get_token
from rest_framework import  exceptions
from django.contrib import auth





class UserRegistration(APIView):
    queryset = CustomUser.objects.none()    
    serializer_class = CustomUserSerializer
    http_method_names=['get','post']
    permission_classes=[AllowAny,]
    def post(self,request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid()
        user = CustomUser(**serializer.validated_data)
        user.save()
        return Response({
            'user':'created'
        })



class ExampleAuth(BaseAuthentication):

    def authenticate(self,request):
        email = request.META.get('HTTP_EMAIL')
        password = request.META.get('HTTP_PASSWORD')
        user = auth.authenticate(request,email=email,password=password)
        if user is None:
            raise  exceptions.AuthenticationFailed('email or password is incorrect')


        
        return (user,None) 
        
        
   
class LoginView(APIView):

    authentication_classes = (ExampleAuth,)
    permission_classes = (IsAuthenticated,)
    
    
    def get(self,request):
        if request.user.is_authenticated:
            return Response({
                'user':'authenticated',
                'email': request.user.email
            })
        else:
            return Response({
               'user' : 'is not authenticated' 
            })
        


class EventList(ListAPIView):
    def get_queryset(self):

        user = self.request.user
        return Event.objects.filter(user=user).order_by('from_time')

    queryset = get_queryset 

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [ExampleAuth,]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['category',]
    ordering_fields = ['category',]





class EventCreate(GenericAPIView):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [ExampleAuth,]
    def post(self,request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid()
        task = Event(**serializer.validated_data)
        task.save()
        return Response(serializer.data)
        
class EventDetail(APIView):
    authentication_classes = [ExampleAuth,]
    permission_classes = [IsAuthenticated,]
    

    def get_object(self,id):
        try:
            task = Event.objects.get(id=id)
            return task
        except:
            raise ValidationError('user doesnt not exists')

    def get(self,request,id,format=None):
        task = self.get_object(id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def delete(self,request,id,format=None):
        task = self.get_object(id)   
        task.delete()
        return Response({
            "task":'deleted'
        })
    
    def put(self,request,id,format=None):
        old_task = self.get_object(id)
        serializer = TaskSerializer(instance=old_task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class ProfilesList(ListAPIView):
    permission_classes = [AllowAny,]
    authentication_classes = [ExampleAuth,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['job_category',]
    



class ProfileDetail(APIView):
    permission_classes = [AllowAny,]
    authentication_classes = [ExampleAuth,]
    serializer_class = ProfileSerializer

    def get_object(self,id):
        try:
            profile = Profile.objects.get(id=id)
        except:
            raise exceptions.ValidationError('This profile doesnt not exists')
        return profile
    def get(self,request,id):
        profile = self.get_object(id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    

    def delete(self,request,id):
        profile = self.get_object(id)
        profile.delete()
        return Response({
            'profile':'deleted'
        })
    
class ProfileCreate(APIView):
    permission_classes = [AllowAny,]
    serializer_class = ProfileCreateSerializer
    authentication_classes = [ExampleAuth,]
    
    def post(self,request):
        serializer = ProfileCreateSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        profile  = Profile(**serializer.validated_data)
        profile.save()
        return Response(serializer.data)
        





     






            





    









