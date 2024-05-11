# publishers.py

import redis
from django.conf import settings

# Initialisation du client Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

def publish_course_update(course):
    """
    Publie une mise à jour du cours dans le canal 'course_updates'.
    
    Args:
    course (Course): L'instance du cours mis à jour.
    """
    message = f'Course Updated: {course.title} by Teacher ID {course.teacher_id}'
    redis_client.publish('course_updates', f'{course.pk}:{message}')

def publish_course_creation(course):
    """
    Publie une création de cours dans le canal 'course_creations'.
    
    Args:
    course (Course): L'instance du cours créé.
    """
    message = f'New Course Created: {course.title} by Teacher ID {course.teacher_id}'
    redis_client.publish('course_creations', f'{course.pk}:{message}')
