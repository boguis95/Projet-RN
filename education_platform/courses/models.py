# courses/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    level = models.CharField(max_length=50)
    max_students = models.PositiveIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses', blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def is_active(self):
        # Assume a course expires after 7 days of no updates or new students
        return (timezone.now() - self.last_updated).days < 7
