# courses/forms.py

from django import forms
from .models import Course, Student, Teacher

class CourseForm(forms.Form):
    title = forms.CharField(max_length=100)
    summary = forms.CharField(widget=forms.Textarea)
    level = forms.CharField(max_length=50)
    max_students = forms.IntegerField(min_value=1)
        

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'user']

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'user']
