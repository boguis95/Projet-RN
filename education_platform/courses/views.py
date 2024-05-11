from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Student, Teacher
from .forms import CourseForm, StudentForm, TeacherForm
from .publishers import publish_course_update, publish_course_creation
from datetime import timedelta
import datetime

# Courses Views
def course_list(request):
    courses = list(Course.all())
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = Course.get(pk)
    return render(request, 'courses/course_detail.html', {'course': course})

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = Course(**form.cleaned_data)
            course.save()
            # Publie une création de cours
            publish_course_creation(course)
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

def course_update(request, course_id):
    course = Course.get(course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            # Publie une mise à jour de cours
            publish_course_update(course)
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})

def course_delete(request, pk):
    course = Course.get(pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# Students Views
def student_list(request):
    students = list(Student.all())
    return render(request, 'courses/student_list.html', {'students': students})

def student_detail(request, pk):
    student = Student.get(pk)
    return render(request, 'courses/student_detail.html', {'student': student})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = Student(**form.cleaned_data)
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'courses/student_form.html', {'form': form})

def student_update(request, pk):
    student = Student.get(pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'courses/student_form.html', {'form': form})

def student_delete(request, pk):
    student = Student.get(pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'courses/student_confirm_delete.html', {'student': student})

# Teachers Views
def teacher_list(request):
    teachers = list(Teacher.all())
    return render(request, 'courses/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = Teacher.get(pk)
    return render(request, 'courses/teacher_detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = Teacher(**form.cleaned_data)
            teacher.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'courses/teacher_form.html', {'form': form})

def teacher_update(request, pk):
    teacher = Teacher.get(pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'courses/teacher_form.html', {'form': form})

def teacher_delete(request, pk):
    teacher = Teacher.get(pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'courses/teacher_confirm_delete.html', {'teacher': teacher})


def enroll_student_in_course(student_id, course_id):
    course = Course.get(course_id)
    student = Student.get(student_id)

    if course.available_slots > 0 and student.pk not in course.student_ids:
        course.student_ids.append(student.pk)
        course.available_slots -= 1
        # Rafraîchir la date d'expiration du cours
        course.expiration_time = datetime.datetime.now() + timedelta(days=7)
        course.save()
        student.enrolled_courses.append(course.pk)
        student.save()
        return True
    return False

# views.py

def student_course_registration(request, student_id, course_id):
    success = enroll_student_in_course(student_id, course_id)
    if success:
        course = Course.get(course_id)
        publish_course_update(course)
        return redirect('course_detail', pk=course_id)
    else:
        return render(request, 'error.html', {'message': 'Failed to enroll in course'})

