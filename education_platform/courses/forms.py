from django import forms
from .models import Course, Student, Teacher

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'teacher_id', 'summary', 'level', 'available_slots', 'student_ids']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'enrolled_courses']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'courses']
