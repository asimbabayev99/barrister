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




class SkillAPIView(APIView):

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
        # Create a skill from the above data
        serializer = SkillSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response({"success": "Skill '{}' created successfully".format(skill_saved.name)})
    

    def put(self, request, pk):
        saved_skill = get_object_or_404(Skill.objects.all(), pk=pk)
        data = request.data
        # print("data -> ", data)
        serializer = SkillSerializer(instance=saved_skill, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response({"success": "Skill '{}' updated successfully".format(skill_saved.name)})


    def delete(self, request, pk):
        # Get object with this pk
        skill = get_object_or_404(Skill.objects.all(), pk=pk)
        skill.delete()
        return Response({"message": "Skill with id `{}` has been deleted.".format(pk)},status=204)





class AwardAPIView(APIView):

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
        data = request.data
        # Create an award from the above data
        serializer = AwardSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            award_saved = serializer.save()
        return Response({"success": "Award '{}' created successfully".format(award_saved.title)})
    

    def put(self, request, pk):
        saved_award = get_object_or_404(Award.objects.all(), pk=pk)
        data = request.data
        serializer = AwardSerializer(instance=saved_award, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            award_saved = serializer.save()
        return Response({"success": "Award '{}' updated successfully".format(award_saved.title)})


    def delete(self, request, pk):
        # Get object with this pk
        award = get_object_or_404(Award.objects.all(), pk=pk)
        award.delete()
        return Response({"message": "Award with id `{}` has been deleted.".format(pk)},status=204)




class ExperienceAPIView(APIView):
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
        # Create an experience from the above data
        serializer = ExperienceSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()
        return Response({"success": "Experience '{}' created successfully".format(experience_saved.title)})
    

    def put(self, request, pk):
        saved_experience = get_object_or_404(EducationAndWorkExperience.objects.all(), pk=pk)
        data = request.data
        serializer = ExperienceSerializer(instance=saved_experience, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()
        return Response({"success": "Experience '{}' updated successfully".format(experience_saved.title)})


    def delete(self, request, pk):
        # Get object with this pk
        experience = get_object_or_404(EducationAndWorkExperience.objects.all(), pk=pk)
        experience.delete()
        return Response({"message": "Experience with id `{}` has been deleted.".format(pk)},status=204)