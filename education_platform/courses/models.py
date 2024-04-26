from django.db import models

# Modèle pour les enseignants
class Teacher(models.Model):
    name = models.CharField(max_length=200)  # Nom de l'enseignant

# Modèle pour les étudiants
class Student(models.Model):
    name = models.CharField(max_length=200)  # Nom de l'étudiant
    # Relation ManyToMany pour les cours auxquels l'étudiant est inscrit
    enrolled_courses = models.ManyToManyField('Course', related_name='students')

# Modèle pour les cours
class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True)  # Identifiant unique du cours
    title = models.CharField(max_length=200)  # Titre du cours
    # Clé étrangère reliant chaque cours à un enseignant spécifique
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    summary = models.TextField()  # Résumé du cours
    level = models.CharField(max_length=100)  # Niveau du cours (débutant, intermédiaire, avancé)
    available_slots = models.IntegerField()  # Nombre de places disponibles dans le cours
