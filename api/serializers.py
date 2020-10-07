from rest_framework import serializers
from account.models import *
from home.models import *

from shop.models import *
# from rest_framework.parsers import 
from django.forms.fields import FileField

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name","email","password","phone_number",]
    def create(self,validated_data):
        user=CustomUser.objects.create(**validated_data)
        user.set_password(validated_data["password"])

        return user



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password']
    def validate(self,data):
        try:
            CustomUser.objects.get(email=data['email'])
        except:
            return serializers.ValidationError('this user not exist')
        return data




class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['name']




class EventCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Event
        fields = ['name','description','location','completed','category','user']
    def create(self,validated_data):
        task = Event(**validated_data)
        task.save()
        return task



class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        models = Event
        fields = ['user','name','description','location','completed','category']

    


class SkillSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    profile_id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)
    progress = serializers.IntegerField() 

    def create(self, validated_data):
        return Skill.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.profile_id = validated_data.get('profile_id', instance.profile_id)
        instance.name = validated_data.get('name', instance.name)
        instance.progress = validated_data.get('progress', instance.progress)

        instance.save()
        return instance

    class Meta:
        model = Skill
        fields = ('pk', 'profile_id', 'name', 'progress')


class AwardSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    profile_id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return Award.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.profile_id = validated_data.get('profile_id', instance.profile_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance



class ExperienceSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    profile = models.IntegerField()
    title = serializers.CharField(max_length=256)
    start = serializers.DateField()
    end = serializers.DateField(required=False)

    def create(self, validated_data):
        return EducationAndWorkExperience.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.profile_id = validated_data.get('profile', instance.profile_id)
        instance.title = validated_data.get('title', instance.title)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)

        instance.save()
        return instance
    
    class Meta:
        model = EducationAndWorkExperience
        fields = ('pk', 'profile', 'title', 'start', 'end')


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    awards = AwardSerializer(many=True)
    class Meta:
        model = Profile
        fields = ['user','image','gender','biography','job_category', 'skills', 'experiences', 'awards']




class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile    
        fields = ['user','gender','job_category','biography']



class PublicationSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField()
    text = serializers.CharField()
    file = serializers.FileField()
    date = serializers.DateTimeField()

    def create(self, validated_data):
        return Publication.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.text = validated_data.get('text', instance.text)
        instance.file = validated_data.get('file', instance.file)
        instance.date = validated_data.get('date', instance.date)

        instance.save()
        return instance




class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    awards = AwardSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'phone_prefix', 
            'phone_number', 'address', 'seriya_type', 'seriya', 'fin', 'profile', 
            'is_active', 'is_superuser', 'is_staff', 'date_joined'
        ]


# class AttachmentSerializer(serializers.ModelSerializer):
#     file = FileField(max_length=None, allow_empty_file=False)

#     class Meta:
#         model = Attachment
#         # fields = ['name', ]
#         fields = '__all__'


# class EmailSerializer(serializers.ModelSerializer):
#     attachments = AttachmentSerializer(many=True)

#     class Meta:
#         model = Email
#         fields = '__all__'
#         # fields = ['folder', 'sender', 'receiver']


class NewsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.FileField()
    
    class Meta:
        model = News
        fields = ['title','content','date','image','user']
    
    def update(self,instance,validated_data):
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.image = validated_data['image']
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title','description','status','deadline',]

    
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title','description','category','color','image','price','discounted_price','stock','date','deleted']


class BasketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = Basket
        fields = ['user','product','quantity']


class EmailAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAccount
        fields = ['token']



class EventSerializer(serializers.ModelSerializer):
    category_bgcolor = serializers.CharField(source='category.bg_color', read_only=True)
    category_textcolor = serializers.CharField(source='category.text_color', read_only=True)
    start = serializers.DateTimeField(format="%m/%d/%Y %H:%M")
    end = serializers.DateTimeField(format="%m/%d/%Y %H:%M")
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = "__all__"



class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_date.get('address', instance.address)
        instance.save()
        return instance

    class Meta:
        model = Contact
        fields = '__all__'
        
    


# serializer with nested contact serializer
class AppointmentContactSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    start = serializers.DateField(format="%d/%m/%Y %H:%M")
    end = serializers.DateField(format="%d/%m/%Y %H:%M")
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.address = validated_data.get('address', instance.address)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance


    class Meta:
        model = Appointment
        fields = '__all__'




class AppointmentSerializer(serializers.ModelSerializer):
    start = serializers.DateField(format="%d/%m/%Y %H:%M")
    end = serializers.DateField(format="%d/%m/%Y %H:%M")
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    def update(self,instance,validated_data):
        instance.contact = validated_data.get('contact', instance.contact)
        instance.status = validated_data.get('status', instance.status)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.address = validated_data.get('address', instance.address)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance


    class Meta:
        model = Appointment
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url',read_only=True)

    class Meta:
        model = Attachment
        fields = ['name','url']


class EmailSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True,read_only=True)
    class Meta:
        model = Email
        fields = ['id','folder','sender','receiver','subject','content','flag','date','num','date','attachments']
        # fields = "__all__"

class EmailFolderMoveSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    from_folder =serializers.CharField(required=True)
    to_folder = serializers.CharField(required=True)


class EmailDeleteSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    folder = serializers.CharField(required=True)