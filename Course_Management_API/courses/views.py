from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Progress
from .serializers import UserSerializer, CourseSerializer, LessonSerializer, ProgressSerializer
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token})
        return Response({'error': 'Invalid credentials'}, status=400)

# courses/views.py
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can create courses.")
        serializer.save(created_by=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can update courses.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_teacher:
            raise PermissionDenied("Only teachers can delete courses.")
        instance.delete()

class ProgressView(generics.ListCreateAPIView):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Progress.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
