import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from chatapp.models import Message  # Replace with your app's Message model

# Dictionary to track active connections
active_connections = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handle the WebSocket connection.
        """
        self.pair_id = self.scope['url_route']['kwargs']['pair_id']
        
        # Add the connection to the active_connections dictionary
        if self.pair_id in active_connections:
            active_connections[self.pair_id].append(self)
        else:
            active_connections[self.pair_id] = [self]
        
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle the WebSocket disconnection.
        """
        if self.pair_id in active_connections:
            active_connections[self.pair_id].remove(self)
            # Remove pair_id from active_connections if no active WebSocket remains
            if not active_connections[self.pair_id]:
                del active_connections[self.pair_id]

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages.
        """
        data = json.loads(text_data)
        await self.handle_message(data)

    async def handle_message(self, data):
        """
        Process the received message and broadcast it to connected clients.
        """
        message_content = data.get("message")
        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        
        if message_content and sender_id:
            try:
                sender = await self.get_user(sender_id)
                receiver = await self.get_user(receiver_id)

                # Prepare the message to send to WebSocket clients
                response_data = {
                    'sender': sender.username,
                    'message': message_content
                }

                # Save the message to the database
                await self.save_message(sender, receiver, message_content)

                # Broadcast message to the WebSocket connections in the pair
                for connection in active_connections.get(self.pair_id, []):
                    await connection.send(text_data=json.dumps(response_data))

            except User.DoesNotExist:
                await self.send(text_data=json.dumps({'error': 'Invalid user or receiver not found'}))

    @database_sync_to_async
    def get_user(self, user_id):
        """
        Fetch the user from the database.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise User.DoesNotExist

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        """
        Save the message to the database.
        """
        Message.objects.create(sender=sender, receiver=receiver, content=content)
