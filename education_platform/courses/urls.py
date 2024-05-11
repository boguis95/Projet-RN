from django.urls import path
from . import views

urlpatterns = [
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:pk>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<str:pk>/update/', views.course_update, name='course_update'),
    path('courses/<str:pk>/delete/', views.course_delete, name='course_delete'),

    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/<str:pk>/', views.student_detail, name='student_detail'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<str:pk>/update/', views.student_update, name='student_update'),
    path('students/<str:pk>/delete/', views.student_delete, name='student_delete'),

    # Teacher URLs
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<str:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<str:pk>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<str:pk>/delete/', views.teacher_delete, name='teacher_delete'),
]
