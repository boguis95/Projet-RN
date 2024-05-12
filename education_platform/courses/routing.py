# courses/routing.py

from django.urls import re_path
from .consumers import CourseConsumer

websocket_urlpatterns = [
    re_path(r'ws/courseupdates/$', CourseConsumer.as_asgi()),
]
