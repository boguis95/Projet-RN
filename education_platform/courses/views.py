# courses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import redis
import json
from .models import Course, Student, Teacher
from .forms import CourseForm, StudentProfileForm, TeacherProfileForm  # Ensure you import the forms here
from datetime import datetime
import pytz 
from django.http import Http404



# Initialize Redis connection
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def list_courses(request):
    course_keys = r.keys('course:*')
    courses = [r.hgetall(course_key) for course_key in course_keys]

    processed_courses = []

    for course in courses:
        # Decode all byte string keys and values
        course_data = {key.decode('utf-8') if isinstance(key, bytes) else key: 
                       value.decode('utf-8') if isinstance(value, bytes) else value 
                       for key, value in course.items()}

        # Convert 'id' and 'max_students' to integers
        course_data['id'] = int(course_data.get('id', 0))
        course_data['max_students'] = int(course_data.get('max_students', 0))

        # Convert 'students' from JSON string back to list
        course_data['students'] = json.loads(course_data.get('students', '[]'))

        # Ensure 'last_updated' is parsed correctly
        if 'last_updated' in course_data:
            last_updated_str = course_data['last_updated']
            last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S.%f")
            course_data['last_updated'] = pytz.utc.localize(last_updated)
        else:
            course_data['last_updated'] = timezone.now()

        # Determine if the course is active
        course_data['is_active'] = (timezone.now() - course_data['last_updated']).days < 7

        # Append to the list of processed courses
        processed_courses.append(course_data)

    print("Processed Courses Data:", processed_courses)  # Debug: Final processed data

    return render(request, 'courses/list_courses.html', {'courses': processed_courses})



def list_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'courses/list_teachers.html', {'teachers': teachers})

def list_students(request):
    students = Student.objects.all()
    return render(request, 'courses/list_students.html', {'students': students})

def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'courses/teacher_detail.html', {'teacher': teacher})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'courses/student_detail.html', {'student': student})



def search_courses(request):
    query = request.GET.get('query', '')
    
    if query:
        # Fetch all courses and filter by title
        course_keys = r.keys('course:*')
        courses = [r.hgetall(key) for key in course_keys]
        filtered_courses = [course for course in courses if query.lower() in course.get('title', '').lower()]
    else:
        filtered_courses = []

    return render(request, 'courses/search_courses.html', {'courses': filtered_courses})



def course_detail(request, course_id):
    # Construct the Redis key for the course
    course_key = f"course:{course_id}"
    
    # Check if the course key exists in Redis
    if not r.exists(course_key):
        raise Http404("No Course matches the given query.")
    
    # Fetch the course data
    course_data = r.hgetall(course_key)
    
    # Convert numerical fields from strings
    course_data['id'] = int(course_data.get('id', course_id))
    course_data['max_students'] = int(course_data.get('max_students', 0))
    
    # Deserialize 'students' list
    student_ids = json.loads(course_data.get('students', '[]'))
    course_data['students'] = Student.objects.filter(id__in=student_ids)
    
    # Fetch the teacher
    teacher_id = course_data.get('teacher_id')
    if teacher_id:
        course_data['teacher'] = Teacher.objects.get(id=teacher_id)
    
    # Handle the form to enroll a new student
    if request.method == 'POST' and 'student_id' in request.POST:
        student_id = request.POST['student_id']
        student = get_object_or_404(Student, id=student_id)
        
        if len(student_ids) < course_data['max_students']:
            student_ids.append(student.id)
            r.hset(course_key, 'students', json.dumps(student_ids))
            
            # Redirect to refresh the page and the data
            return redirect('courses:course_detail', course_id=course_id)

    # All students not currently enrolled in this course
    students = Student.objects.exclude(id__in=student_ids)
    
    return render(request, 'courses/course_detail.html', {
        'course': course_data,
        'students': students
    })




def enroll_course(request, course_id):
    # Construct the Redis key for the course
    course_key = f"course:{course_id}"
    
    # Check if the course key exists in Redis
    if not r.exists(course_key):
        raise Http404("No Course matches the given query.")
    
    # Fetch the course data
    course_data = r.hgetall(course_key)
    
    # Convert numerical fields from strings
    course_data['id'] = int(course_data.get('id', course_id))
    course_data['max_students'] = int(course_data.get('max_students', 0))
    
    # Deserialize 'students' list
    course_data['students'] = json.loads(course_data.get('students', '[]'))
    
    # Check if the user is trying to enroll (this is a simplified logic example)
    if request.method == 'POST':
        # Example: Get or create a student (this is a placeholder logic)
        student_id = request.POST.get('student_id')
        student, _ = Student.objects.get_or_create(id=student_id, defaults={'name': f"Student {student_id}"})
        
        # Check if the course can accept more students
        if len(course_data['students']) < course_data['max_students']:
            # Enroll the student by adding them to the course's student list
            course_data['students'].append(student.id)
            
            # Save the updated students list back to Redis
            r.hset(course_key, 'students', json.dumps(course_data['students']))
            
            # Redirect to the course detail page
            return redirect('courses:course_detail', course_id=course_data['id'])
        else:
            return render(request, 'courses/enroll_course.html', {'error': 'This course is full', 'course': course_data})

    return render(request, 'courses/enroll_course.html', {'course': course_data})




def update_course(request, course_id):
    # Construct the Redis key for the course
    course_key = f"course:{course_id}"
    
    # Check if the course key exists in Redis
    if not r.exists(course_key):
        raise Http404("No Course matches the given query.")
    
    # Fetch the course data
    course_data = r.hgetall(course_key)
    
    # Convert numerical fields
    course_data['id'] = int(course_data.get('id', course_id))
    course_data['max_students'] = int(course_data.get('max_students', 0))
    course_data['students'] = json.loads(course_data.get('students', '[]'))
    
    # Handle POST request: Update course data
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # Update course fields based on form data
            course_data.update({
                'title': form.cleaned_data['title'],
                'summary': form.cleaned_data['summary'],
                'level': form.cleaned_data['level'],
                'max_students': form.cleaned_data['max_students'],
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            })
            # Save updated course data to Redis
            r.hmset(course_key, course_data)
            return redirect('courses:course_detail', course_id=course_data['id'])
    else:
        # Initialize form with existing course data for GET request
        form = CourseForm(initial=course_data)
    
    return render(request, 'courses/update_course.html', {'form': form, 'course_id': course_id})


def update_profile(request):
    if hasattr(request.user, 'student'):
        profile = request.user.student
        ProfileForm = StudentProfileForm
    else:
        profile = request.user.teacher
        ProfileForm = TeacherProfileForm

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'courses/update_profile.html', {'form': form})


def home(request):
    return render(request, 'home.html')