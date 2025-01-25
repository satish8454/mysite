# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.receiver_id = self.scope['url_route']['kwargs']['user_id']
        
        # Channel name for the user connection
        self.room_group_name = f'chat_{min(self.user_id, self.receiver_id)}_{max(self.user_id, self.receiver_id)}'
        
        # Join the WebSocket group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print("Hi")
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['reciever_id']

        # Get the sender and receiver users
        sender = User.objects.get(id=self.user_id)
        receiver = User.objects.get(id=receiver_id)
        
        # Save the message to the database
        chat_message = Message(sender=sender, receiver=receiver, content=message)
        chat_message.save()

        # Send the message to WebSocket (broadcasting to the other user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    # Receive message from WebSocket
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
