# courses/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CourseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("course_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("course_updates", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            "course_updates",
            {
                'type': 'send_course_update',
                'message': message
            }
        )

    async def send_course_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
s