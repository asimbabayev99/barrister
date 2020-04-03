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
        return Event.objects.filter(user=user).order_by('start')

    queryset = get_queryset 

    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [ExampleAuth,]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['category',]
    ordering_fields = ['category',]





class EventCreate(GenericAPIView):
    queryset = Event.objects.none()
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [ExampleAuth,]
    def post(self,request):
        serializer = EventCreateSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        event = Event(**serializer.validated_data)
        event.save()
        return Response(serializer.data)



class EventDetail(APIView):
    authentication_classes = [ExampleAuth,]
    permission_classes = [IsAuthenticated,]
    
    
    def get_object(self,id):
        try:
            event = Event.objects.get(id=id,user=self.request.user)
            return event
        except:
            raise serializers.ValidationError('event doesnt not exists')

    def get(self,request,id,format=None):
        event = self.get_object(id)
        serializer = EventCreateSerializer(event)
        return Response(serializer.data)
    
    def delete(self,request,id,format=None):
        event = self.get_object(id)   
        event.delete()
        return Response({
            "event":'deleted'
        })
    


    
    def put(self,request,id,format=None):
        old_event = self.get_object(id)
        serializer = EventCreateSerializer(instance=old_event,data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
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
        if request.user == profile.user:
            profile.delete()
            return Response({
                'profile':'deleted'
            })
        else:
            return Response({
                'permission':'denied'
            })
     
    def put(self,request,id):
        profile = self.get_object(id)
        data = request.data
        if profile.user != request.user:
            return Response({
                'permission':'denied'
            }) 
        serializer = ProfileCreateSerializer(profile,data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'profile':'updated'
            
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
        





     


    










class SkillAPIView(APIView):

    authentication_classes = [ExampleAuth,]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.GET.get('profile')
        if profile:
            skills = Skill.objects.filter(profile__id=profile)
        else:
            skills = Skill.objects.all()
        # the many param informs the serializer that it will be serializing more than a single skill.
        serializer = SkillSerializer(skills, many=True)
        return Response({"skills": serializer.data})


    def post(self, request):
        data = request.data
        profile = Profile.objects.get(id=data.get('profile_id'))
        if profile.user != request.user:
            return Response({"detail": "Permission denied"}, status=403)
        # Create a skill from the above data
        serializer = SkillSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response({"success": "Skill '{}' created successfully".format(skill_saved.name)})
    

    def put(self, request, pk):
        saved_skill = get_object_or_404(Skill.objects.all(), pk=pk)
        data = request.data
        if request.user != saved_skill.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        serializer = SkillSerializer(instance=saved_skill, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response({"success": "Skill '{}' updated successfully".format(skill_saved.name)})


    def delete(self, request, pk):
        # Get object with this pk
        skill = get_object_or_404(Skill.objects.all(), pk=pk)
        if request.user != skill.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        skill.delete()
        return Response({"message": "Skill with id `{}` has been deleted.".format(pk)},status=204)





class AwardAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.GET.get('profile')
        if profile:
            awards = Award.objects.filter(profile__id=profile)
        else:
            awards = Award.objects.all()
        # the many param informs the serializer that it will be serializing more than a single award.
        serializer = AwardSerializer(awards, many=True)
        return Response({"awards": serializer.data})


    def post(self, request):
        profile = Profile.objects.get(id=data.get('profile_id'))
        if request.user != profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        data = request.data
        # Create an award from the above data
        serializer = AwardSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            award_saved = serializer.save()
        return Response({"success": "Award '{}' created successfully".format(award_saved.title)})
    

    def put(self, request, pk):
        saved_award = get_object_or_404(Award.objects.all(), pk=pk)
        if request.user != saved_award.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        data = request.data
        serializer = AwardSerializer(instance=saved_award, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            award_saved = serializer.save()
        return Response({"success": "Award '{}' updated successfully".format(award_saved.title)})


    def delete(self, request, pk):
        # Get object with this pk
        award = get_object_or_404(Award.objects.all(), pk=pk)
        if request.user != award.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        award.delete()
        return Response({"message": "Award with id `{}` has been deleted.".format(pk)},status=204)




class ExperienceAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = request.GET.get('profile')
        if profile:
            experiences = ExperienceAPIView.objects.filter(profile__id=profile)
        else:
            experiences = ExperienceAPIView.objects.all()
        # the many param informs the serializer that it will be serializing more than a single experience.
        serializer = ExperienceSerializer(experiences, many=True)
        return Response({"experiences": serializer.data})


    def post(self, request):
        data = request.data
        profile = Profile.objects.get(id=data.get('profile_id'))
        if request.user != profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        # Create an experience from the above data
        serializer = ExperienceSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()
        return Response({"success": "Experience '{}' created successfully".format(experience_saved.title)})
    

    def put(self, request, pk):
        saved_experience = get_object_or_404(EducationAndWorkExperience.objects.all(), pk=pk)
        if request.user != saved_experience.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        data = request.data
        serializer = ExperienceSerializer(instance=saved_experience, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()
        return Response({"success": "Experience '{}' updated successfully".format(experience_saved.title)})


    def delete(self, request, pk):
        # Get object with this pk
        experience = get_object_or_404(EducationAndWorkExperience.objects.all(), pk=pk)
        if request.user != experience.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        experience.delete()
        return Response({"message": "Experience with id `{}` has been deleted.".format(pk)},status=204)