import redis
import json
from datetime import datetime

def initialize_redis():
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    # Reset any existing data
    r.flushdb()

    # Initialize auto-increment counters for each entity type
    r.set('teacher_id', 2)
    r.set('student_id', 3)
    r.set('course_id', 3)

    # Sample data for teachers, students, and courses
    teachers = [
        {"id": 1, "name": "John Doe", "user_id": 1},
        {"id": 2, "name": "Jane Smith", "user_id": 2}
    ]

    students = [
        {"id": 1, "name": "Student One", "user_id": 3},
        {"id": 2, "name": "Student Two", "user_id": 4},
        {"id": 3, "name": "Student Three", "user_id": 5}
    ]

    courses = [
        {"id": 1, "title": "Math 101", "summary": "Introductory Math", "level": "Beginner", "max_students": 2, "teacher_id": 1, "students": [], "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")},
        {"id": 2, "title": "English 101", "summary": "Introductory English", "level": "Beginner", "max_students": 2, "teacher_id": 2, "students": [], "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")},
        {"id": 3, "title": "History 101", "summary": "Introductory History", "level": "Beginner", "max_students": 2, "teacher_id": 1, "students": [1, 2], "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}
    ]

    # Inserting teachers, students, and courses into Redis
    for teacher in teachers:
        r.hset(f"teacher:{teacher['id']}", mapping=teacher)

    for student in students:
        r.hset(f"student:{student['id']}", mapping=student)

    for course in courses:
        course_data = {**course, "students": json.dumps(course["students"])}
        r.hset(f"course:{course['id']}", mapping=course_data)

    print("Redis has been initialized with sample data.")

if __name__ == "__main__":
    initialize_redis()
