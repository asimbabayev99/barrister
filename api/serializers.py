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
        fields = ['user','name','description','loccation','complated','category']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','image','gender','biography','job_category']

class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile    
        fields = ['user','gender','job_category','biography']
    

class SkillSerializer(serializers.Serializer):
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



class ExperienceSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    profile_id = models.IntegerField()
    title = serializers.CharField(max_length=256)
    start = serializers.DateField()
    end = serializers.DateField(required=False)

    def create(self, validated_data):
        return EducationAndWorkExperience.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.profile_id = validated_data.get('profile_id', instance.profile_id)
        instance.title = validated_data.get('title', instance.title)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)

        instance.save()
        return instance