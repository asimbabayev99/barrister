from django.shortcuts import render
from dateutil.relativedelta import relativedelta
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAdminUser
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
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import *
from shop.models import *
from account.tasks import *
import logging


class UserAPI(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def get_object(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except:
            raise exceptions.ValidationError('This user doesnt not exists')
        return user

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    class Meta:
        models = CustomUser
        fields = '__all__'


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
                'detail':'Permission denied'
            },status=403)
     
    def put(self,request,id):
        profile = self.get_object(id)
        data = request.data
        if profile.user != request.user:
            return Response({
                'detail':'Permission denied'
            }, status=403) 
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

    authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAuthenticated]

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
        return Response(serializer.data)
    

    def put(self, request, pk):
        saved_skill = get_object_or_404(Skill.objects.all(), pk=pk)
        data = request.data
        if request.user != saved_skill.profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        serializer = SkillSerializer(instance=saved_skill, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            skill_saved = serializer.save()
        return Response(serializer.data)


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
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = request.GET.get('profile')
        if profile:
            experiences = EducationAndWorkExperience.objects.filter(profile__id=profile)
        else:
            experiences = EducationAndWorkExperience.objects.all()
        # the many param informs the serializer that it will be serializing more than a single experience.
        serializer = ExperienceSerializer(experiences, many=True)
        return Response({"experiences": serializer.data})


    def post(self, request):
        data = request.data
        profile = Profile.objects.get(id=data.get('profile'))
        if request.user != profile.user:
            return Response({"detail": "Permission denied"}, status=403)
        # Create an experience from the above data
        serializer = ExperienceSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            experience_saved = serializer.save()
        # return Response({"success": "Experience '{}' created successfully".format(experience_saved.title)})
        return Response(serializer.data)
    

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



class PublicationListView(ListAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny,]
    





class PublicationAPIView(APIView):

    items_per_page = 24
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = PublicationSerializer
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        page = request.query_params.get('page', 1)
        publications = Publication.objects.all()
        paginator = Paginator(publications, self.items_per_page)
        serializer = self.serializer_class(paginator.get_page(page), many=True)

        return Response({"publications": serializer.data}, status=200)


    def post(self, request):
        data = request.data
        permission = Permission.objects.get(codename='add_publication')
        if request.user.role is None or permission not in request.user.role.permissions:
            return Response({"detail": "Permission denied"}, status=403)
        # Create an experience from the above data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            publication_saved = serializer.save()
        return Response({"success": "Publication '{}' created successfully".format(publication_saved.pk)})
    

    def put(self, request, pk):
        saved_publication = get_object_or_404(Publication.objects.all(), pk=pk)
        permission = Permission.objects.get(codename='change_publication')
        if request.user.role is None or permission not in request.user.role.permissions:
            return Response({"detail": "Permission denied"}, status=403)
        data = request.data
        serializer = self.serializer_class(instance=saved_publication, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            publication_saved = serializer.save()
        return Response({"success": "Publication '{}' updated successfully".format(publication_saved.pk)})


    def delete(self, request, pk):
        # Get object with this pk
        publication = get_object_or_404(Publication.objects.all(), pk=pk)
        permission = Permission.objects.get(codename='delete_publication')
        if request.user.role is None or permission not in request.user.role.permissions:
            return Response({"detail": "Permission denied"}, status=403)

        publication.delete()
        return Response({"message": "Publication with id `{}` has been deleted.".format(pk)},status=204)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000

class NewsList(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # authentication_classes = [ExampleAuth,]
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    pagination_class = StandardResultsSetPagination
    


class NewsAPI(APIView):
    # authentication_classes=[ExampleAuth]
    permission_classes = [AllowAny]
    

    def get_object(self,pk):
        news = get_object_or_404(News.objects.all(),pk=pk)
        return news
    
    def get(self,request,pk):
        news = self.get_object(pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        data = request.data
        serializer = NewsSerializer(data=data,context={'request':request},)
        permission = Permission.objects.get(codename="add_news")
        if request.user.is_superuser == False:
            return Response({"permission":'denied'})
        if serializer.is_valid(raise_exception=True):
            news = News(**serializer.validated_data)
            news.save()
        return Response({"detail" : "publication {} saved".format(news.pk)})
    
    def put(self,request,pk):
        old_news = self.get_object(pk)
        data  = request.data
        serializer = NewsSerializer(old_news,data,context={'request':request})
        # permission = Permission.objects.get(codename="update_news")
        # if request.user.role is None or permission not in request.user.role.permissions.all():
        #     return Response({"permission":'denied'})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        news = self.get_object(pk)
        serializer = NewsSerializer(news)
        # permission = Permission.objects.get(codename='can_delete_news')
        if request.user.has_perm('news.can_delete_news') == False or request.user.role is None or request.user != news.user:
            return Response({'permission':'denied'})
        news.delete()
        return Response({'news':'deleted'})

            
class TaskList(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication,]
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    pagination_class = StandardResultsSetPagination
    

class TaskDetail(APIView):
    authentication_classes=[ExampleAuth]
    permission_classes = [IsAuthenticated]
    
    def get_object(self,pk):
        task = get_object_or_404(Task.objects.all(),pk=pk)
        return task
    
    def get(self,request,pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = Task()
            task.title = serializer.validated_data['title']
            task.description = serializer.validated_data['description']
            task.status = serializer.validated_data['status']
            task.user = request.user
            task.deadline = serializer.validated_data['deadline']
            task.save()
        return Response({'task':'created'})


    
    def put(self,request,pk):
        old_task = self.get_object(pk)
        data = request.data
        serializer = TaskSerializer(old_task,data)
        if serializer.is_valid():
            serializer.save()
        return Response({'task':'updated'})        

    
    def delete(self,request,pk):
        task = self.get_object(pk)
        task.delete()
        return Response({'task':'deleted'})
        

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [ExampleAuth,]
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    pagination_class = StandardResultsSetPagination



class BasketList(ListAPIView):
    def get_queryset(self):
        queryset = Basket.objects.filter(user=self.request.user)
        return queryset
    queryset = get_queryset
    serializer_class  = BasketSerializer
    permission_classes = [AllowAny,]
    authentication_classes = [SessionAuthentication,ExampleAuth]



class BasketDetail(APIView):
    # authentication_classes=[SessionAuthentication]
    # permission_classes = [IsAuthenticated,AllowAny]

    def get(self,request,pk):
        basket = get_object_or_404(Basket.objects.all(),pk=pk)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        if Basket.objects.filter(user=request.user, product__id=data['product']).exists():
            return Response({'detail': 'You already have this item in basket'}, status=400)
        serializer = BasketSerializer(data=data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'Basket item saved successfully'})
    
    def delete(self,request,pk):
        basket = get_object_or_404(Basket.objects.filter(),pk=pk)
        if basket.user == request.user:
            basket.delete()
            return Response({'detail':'basket item deleted'})
        else:
            return Response({'detail':'You do not have permissions to delete this item'}, status=403)
    
    def patch(self,request,pk):
        basket = get_object_or_404(Basket.objects.all(),pk=pk)
        if basket.user == request.user:
            serializer = BasketSerializer(basket,request.data,partial=True,context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({'detail':'basket item updated'})
        else:
            return Response({'detail':'You do not have permissions to delete this item'}, status=403)
            

class EmailAccountToken(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes =  [SessionAuthentication,]
    def post(self,request):
        data = request.data
        email = get_object_or_404(EmailAccount.objects.all(),user=request.user)
        if email.token is not None:
            return Response({'token':'exists'})
        serializer = EmailAccountSerializer(data=request.data)
        if serializer.is_valid():
            email.token = serializer.validated_data['token']
            email.save()
            return Response({'token':'saved'})
        return Response({'error':'occured'})




class AppointmentListView(ListAPIView):

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    pagination_class = None

    def get_queryset(self):
        date = self.request.GET.get('date')
        if not date:
            date = datetime(datetime.today().year, 1, 1).date()
        return Appointment.objects.filter(user=self.request.user, start__gte=date)



class AppointmentAPIView(APIView):

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    
    
    def get(self, request, id):
        appointment = get_object_or_404(Appointment.objects.all(), id=id)
        serializer = self.serializer_class(appointment)
        return Response(serializer.data)
    
    def post(self, request):
        # check permissions
        user_permissions = request.user.get_group_permissions()
        if 'home.add_appointment' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403) 

        context = {
            "request": self.request,
        }
        if isinstance(request.data.get('contact'), dict):
            serializer = AppointmentContactSerializer(data=request.data, context=context)
        else:
            serializer = self.serializer_class(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


    def put(self, request, id):
        # check permissions
        saved_obj = get_object_or_404(Appointment.objects.all(), id=id)
        user_permissions = request.user.get_group_permissions()
        if 'home.change_appointment' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403)    
    
        serializer = self.serializer_class(instance=saved_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, id):
        # check permissions
        obj = get_object_or_404(Appointment.objects.all(), id=id)
        user_permissions = request.user.get_group_permissions()
        if 'home.delete_appointment' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403)
        # Get object with this id
        obj.delete()
        return Response({"message": "Object with id `{}` has been deleted.".format(id)}, status=204)





class ContactListView(ListAPIView):

    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Contact.objects.filter(user=request.user).order_by('-date')



class ContactAPIView(APIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]

    def get(self, request, id):
        contact = get_object_or_404(Contact.objects.all(), id=id)
        serializer = self.serializer_class(contact)
        return Response(serializer.data)

    def post(self, request):
        # check permissions
        user_permissions = request.user.get_group_permissions()
        if 'home.add_contact' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403) 

        context = {
            "request": self.request,
        }
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)

    
    def put(self, request):
        # check permissions
        saved_obj = get_object_or_404(Contact.objects.all(), id=id)
        user_permissions = request.user.get_group_permissions()
        if 'home.change_contact' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403)    
    
        serializer = self.serializer_class(instance=saved_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        # check permissions
        obj = get_object_or_404(Contact.objects.all(), id=id)
        user_permissions = request.user.get_group_permissions()
        if 'home.delete_contact' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403)
        # Get object with this id
        obj.delete()
        return Response({"message": "Object with id `{}` has been deleted.".format(id)}, status=204)




    

class EventListView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    pagination_class = None

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if not start_date:
            start_date = datetime(datetime.today().year, 1, 1)
        if not end_date:
            end_date = datetime(datetime.today().year, 12, 31)
        return Event.objects.filter(user=self.request.user, end__date__gte=start_date, start__date__lte=end_date)



class EventAPIView(APIView):

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]

    def get(self, request, id):
        event = get_object_or_404(Event.objects.all(), id=id)
        serializer = self.serializer_class(event)
        return Response(serializer.data)
    

    def post(self, request):
        # check permissions
        user_permissions = request.user.get_group_permissions()
        if 'home.add_event' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403) 

        context = {
            "request": self.request,
        }
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


    def put(self, request, id):
        # check permissions
        saved_obj = get_object_or_404(Event.objects.all(), id=id)
        user_permissions = request.user.get_group_permissions()
        if 'home.change_event' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403)    
    
        serializer = self.serializer_class(instance=saved_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, id):
        # check permissions
        obj = get_object_or_404(Event.objects.all(), id=id)
        user_permissions = request.user.get_group_permissions()
        if 'home.delete_event' not in user_permissions:
            return Response({"detail": "Permission denied"}, status=403)
        # Get object with this id
        obj.delete()
        return Response({"message": "Object with id `{}` has been deleted.".format(id)}, status=204)



class EmailList(ListAPIView):

    def get_queryset(self):
        user = self.request.user
        return Email.objects.filter(user=user).prefetch_related('attachments')
    
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ['sender', 'receiver']
    ordering_fields = ['date',]



class EmailDetail(APIView):
    # authentication_classes = [SessionAuthentication,]
    # permission_classes = [IsAuthenticated,]
    
    def get_object(self,id):
        try:
            email = Email.objects.get(id=id, user=self.request.user).prefetch_related('attachments')
            return email
        except:
            raise serializers.ValidationError('event doesnt not exists')

    def get(self, request, id, format=None):
        email = self.get_object(id)
        serializer = EmailSerializer(email)
        return Response(serializer.data)


import imapclient

class EmailFolderMove(APIView):
    
    def post(self,request):
        start = datetime.now()
        serializer = EmailFolderMoveSerializer(data=request.data)
        serializer.is_valid()
        # email = get_object_or_404(Email.objects.all(),num=serializer.validated_data['uid'])
        mail_uids = serializer.validated_data['uid']
        print(mail_uids)
        from_folder = serializer.validated_data['from_folder']
        to_folder = serializer.validated_data['to_folder']
        client = imapclient.IMAPClient('imap.yandex.ru')
        print(client.oauth2_login('azadmammedov@yandex.com','AgAAAAA9U6WoAAZmeTTDasOXdE9usp_-zAmOL_E'))
        client.select_folder('{}'.format(from_folder))
        result = client.move(mail_uids,to_folder)
        client.select_folder(to_folder)
        new_folder_mails = client.search('All')
        #adding last mails to database
        # for i in new_folder_mails[len(new_folder_mails)-len(mail_uids):len(new_folder_mails)]:
        

        return ValidationError('mail not moved')
        
        


class EmailDeleteView(APIView):

    def post(self,request):
        start = datetime.now()
        serializer = EmailDeleteSerializer(data=request.data)
        serializer.is_valid()
        messages_list = serializer.validated_data['uids']
        print(messages_list)
        folder = serializer.validated_data['folder']
        client = zimapclient.IMAPClient('imap.yandex.ru')
        try:
            client.oauth2_login('azadmammedov@yandex.com','AgAAAAA9U6WoAAZmeTTDasOXdE9usp_-zAmOL_E')
        except:
            raise ValidationError('auth error')
        client.select_folder(folder) 
        client.delete_messages(messages_list)
        for i in messages_list:
            Email.objects.filter(num=i,folder=folder).delete() 
        end = datetime.now() - start
        return Response({'emails':'deleted in {}'.format(end)})
