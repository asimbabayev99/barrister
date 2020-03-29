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

class CustomAuthToken(ObtainAuthToken):
    serializer_class=LoginSerializer
    permission_classes = [AllowAny,]
    def post(self,request,*args,**kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        try:
            user = CustomUser.objects.get(email=serializer.data['email'])
        except:
            return Response({
              'user':'doesnt not exists'  
            })
        token,created = Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user': user.id,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name
        })





class UserRegistration(viewsets.ModelViewSet):
    queryset = CustomUser.objects.none()    
    serializer_class = CustomUserSerializer
    http_method_names=['get','post']
    permission_classes=[AllowAny,]
    def create(self,request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid()
        if CustomUser.objects.filter(email=serializer.data['email']).exists():
            return Response({
                'user':'already exists'
            })
        else:
            user = CustomUser(**serializer.validated_data)
            user.save()
            token,created = Token.objects.get_or_create(user=user)
            return Response({
                'user':'created',
                'token':token.key
            })


class EventList(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['category',]
    ordering_fields = ['category',]


class EventCreate(GenericAPIView):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid()
        task = Event(**serializer.validated_data)
        task.save()
        return Response(serializer.data)
        
class EventDetail(APIView):

    def get_object(self,id):
        try:
            task = Event.objects.get(id=id)
            return task
        except:
            raise ValidationError('user doesnt not exists')

    def get(self,request,id,format=None):
        task = self.get_object(id)
        serializer = EventSerializer(task)
        return Response(serializer.data)
    
    def delete(self,request,id,format=None):
        task = self.get_object(id)   
        task.delete()
        return Response({
            "event":'deleted'
        })
    
    def put(self,request,id,format=None):
        old_task = self.get_object(id)
        serializer = EventSerializer(instance=old_task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)



