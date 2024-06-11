from rest_framework import serializers
from .models import User, Course, Lesson, Progress

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_student', 'is_teacher')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        #fields = ('id', 'name', 'description', 'created_by')
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'course', 'content')

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id', 'user', 'course', 'progress')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_student', 'is_teacher')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            is_student=validated_data['is_student'],
            is_teacher=validated_data['is_teacher']
        )
        return user        
