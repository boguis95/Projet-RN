# script pour initialiser des données (init_data.py)

from courses.models import Student, Teacher, Course
from datetime import datetime, timedelta

# Créer des enseignants
teacher1 = Teacher(name="Mr. John Doe").save()
teacher2 = Teacher(name="Ms. Jane Smith").save()

# Créer des étudiants
student1 = Student(name="Student One").save()
student2 = Student(name="Student Two").save()
student3 = Student(name="Student Three").save()


# Créer des cours
course1 = Course(
    title="Mathematics 101",
    teacher_id=teacher1.pk,
    summary="An introduction to mathematics.",
    level="Beginner",
    available_slots=30,
    student_ids=[],
    expiration_time=datetime.now() + timedelta(days=30)
).save()

course2 = Course(
    title="History 101",
    teacher_id=teacher2.pk,
    summary="An introduction to World History.",
    level="Beginner",
    available_slots=30,
    student_ids=[],
    expiration_time=datetime.now() + timedelta(days=30)
).save()

# Associer les cours avec les enseignants
teacher1.courses.append(course1.pk)
teacher1.save()

teacher2.courses.append(course2.pk)
teacher2.save()

