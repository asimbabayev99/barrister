from rest_framework import serializers
from account.models import *
from home.models import *


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


class EventSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(many=False,read_only=False,queryset=TaskCategory.objects.all())
    class Meta:
        model = Event
        fields = ['name','description','location','completed','category']
    def create(self,validated_data):
        task = Event(**validated_data)
        task.save()
        return task



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','image','gender','contacts','skills','biography','job_category']

class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile    
        fields = ['user','gender','contacts','skills','job_category']
    
    