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
from rest_framework.authentication import SessionAuthentication , BasicAuthentication
from django.contrib.auth import authenticate,login

# class CustomAuthToken(ObtainAuthToken):
#     serializer_class=LoginSerializer
#     permission_classes = [AllowAny,]
#     def post(self,request,*args,**kwargs):

#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid()
#         try:
#             user = CustomUser.objects.get(email=serializer.data['email'])
#         except:
#             return Response({
#               'user':'doesnt not exists'  
#             })
#         token,created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token':token.key,
#             'user': user.id,
#             'email':user.email,
#             'first_name':user.first_name,
#             'last_name':user.last_name
#         })





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
        
        
class LoginView(APIView):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        user = authenticate(request,email=serializer.data['email'],password=serializer.data['password'])
        if not user:
            return Response({
                'error':'incorrect email or password'
            })
        else:
            login(request,user)
            return Response({
                'user':'login'
            })
        


class EventList(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
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
        event = Event(**serializer.validated_data)
        event.save()
        return Response(serializer.data)



class EventDetail(APIView):

    def get_object(self,id):
        try:
            event = Event.objects.get(id=id)
            return event
        except:
            raise ValidationError('user doesnt not exists')

    def get(self,request,id,format=None):
        event = self.get_object(id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def delete(self,request,id,format=None):
        event = self.get_object(id)   
        event.delete()
        return Response({
            "event":'deleted'
        })
    
    def put(self,request,id,format=None):
        old_event = self.get_object(id)
        serializer = EventSerializer(instance=old_event,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)



