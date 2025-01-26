import os
import django
from channels.db import database_sync_to_async

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Replace 'mysite' with your project name
django.setup()

import asyncio
import websockets
import json
from django.contrib.auth.models import User
from chatapp.models import Message  # Replace with your app's Message model

# Dictionary to track active connections
active_connections = {}

PORT = int(os.environ.get("PORT", 8000))

async def chat_server(websocket, path):
    """
    WebSocket handler to manage chat messages.
    """
    try:
        pair_id = path.strip('/').split('/')[-1]
        if pair_id in active_connections:
            active_connections[pair_id].append(websocket)
        else:
            active_connections[pair_id] = [websocket]
        while True:
            # Listen for messages from the WebSocket
            message = await websocket.recv()
            data = json.loads(message)
            await handle_message(data, websocket,pair_id)

    except User.DoesNotExist:
        await websocket.close()
        print("Invalid user ID")
    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed for user {pair_id}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if pair_id in active_connections:
            active_connections[pair_id].remove(websocket)
            if not active_connections[pair_id]:
                del active_connections[pair_id] 

async def get_user(user_id):
    """
    Fetch user from the database.
    """
    try:
        return await database_sync_to_async(User.objects.get)(id=user_id)
    except Exception as e:
        print(e)

def get_pair_id(user1_id, user2_id):
    """
    Generate a unique pair ID to ensure a connection is specific to a user pair.
    """
    return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

async def handle_message(data, websocket,pair_id):
    """
    Process received messages and broadcast them or store them in the DB.
    """
    message_content = data.get("message")
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    if message_content and sender_id:
        try:
            receiver = await get_user(receiver_id)
            sender = await get_user(sender_id)

            # Prepare message
            response_data = {
                'sender': sender.username,
                'message': message_content
            }
            
            await save_message(sender, receiver, message_content)
            for i in active_connections[pair_id]:
                await i.send(json.dumps(response_data))
        except User.DoesNotExist:
            await websocket.send(json.dumps({'error': 'Invalid user or receiver not found'}))

async def save_message(sender, receiver, content):
    """
    Save message to the database if receiver is offline.
    """
    await database_sync_to_async(Message.objects.create)(sender=sender, receiver=receiver, content=content)

async def start_ws_server():
    """
    Start the WebSocket server.
    """
    print("Starting WebSocket server...")
    async with websockets.serve(chat_server, "localhost", PORT):
        print("WebSocket server started on ws://localhost:8000")
        await asyncio.Future()  # Keep the server running indefinitely

if __name__ == "__main__":
    asyncio.run(start_ws_server())
