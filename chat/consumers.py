
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from channels.exceptions import DenyConnection
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict

from asgiref.sync import async_to_sync
from chat.models import Message
from .views import get_last_10_messages
import json
User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        self.user = self.scope['user']
        self.in_room = self.inGroup(self.room_group_name,self.user)
        if self.in_room == True:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            
            self.accept()           
        else:
            raise DenyConnection("Invalid User")
    
    def inGroup(self,room_group_name,user):
        print("connected")
        return user.groups.filter(name=room_group_name).exists()


    def save_message(self,text):
        Message.objects.create(
            message=text,
            sender=self.scope['user'],
            room=Group.objects.get(name=self.room_name)
        )
        
    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        if(text_data_json['type'] == 'init_messages'):
            self.init_messages()

        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,{
                    'type': text_data_json['type'],
                    'message':message,
                    'user': text_data_json['user']
                }
            )
        print("sended")

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        self.send(text_data=json.dumps({
            'message': message,
            'user':user
        }))
        if(user == self.scope['user'].username):
            self.save_message(message)

    
    def init_messages(self):
        messages =  get_last_10_messages(self.room_name)
        print("here")
        messages = self.parse_messages(messages)
        self.send(text_data=json.dumps({
            'messages':messages,
            'type':"fetched_messages"
        }))
    
    def parse_messages(self,messages):
        result = []
        for message in messages:
            result.append(self.parse_message(message))
        return result

 
    def parse_message(self,message):
        return {
            'message':message.message,
            'user':message.sender.username
        }

