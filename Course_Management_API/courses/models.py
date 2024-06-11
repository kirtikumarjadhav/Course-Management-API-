from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    content = models.TextField()

class Progress(models.Model):
    user = models.ForeignKey(User, related_name='progresses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='progresses', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)