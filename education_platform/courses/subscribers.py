# subscribers.py

import redis
from django.conf import settings
from .models import Course

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

def course_updates_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(['course_updates', 'course_creations'])

    print("Starting to listen on 'course_updates' and 'course_creations' channels...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print("Received message:", message['data'])
            course_id, update_message = message['data'].split(':', 1)
            try:
                course = Course.get(course_id)
                print(f"Course Title: {course.title}, Details: {update_message}")
            except Course.DoesNotExist:
                print("Course not found")
