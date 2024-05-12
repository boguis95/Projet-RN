# courses/urls.py

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.list_courses, name='list_courses'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('search/', views.search_courses, name='search_courses'),
    path('update_course/<int:course_id>/', views.update_course, name='update_course'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('teachers/', views.list_teachers, name='list_teachers'),
    path('students/', views.list_students, name='list_students'),
    path('teacher/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
]
