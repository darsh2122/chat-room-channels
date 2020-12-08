import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room
from django.contrib.auth import get_user_model
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async
from django.contrib.auth.models import Group

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        self.room_group_name = self.room_name
        self.user = self.scope['user']
        self.in_room = await self.inGroup(self.room_group_name,self.user)
        if self.in_room == True:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        else:
            raise DenyConnection("Invalid User")
        

    @database_sync_to_async
    def inGroup(self,room_group_name,user):
        return user.groups.filter(name=room_group_name).exists()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))