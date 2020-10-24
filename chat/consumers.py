from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from account.models import CustomUser
from chat.models import Message, Attachment
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        print("connect")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(data)
        message_type = data['message_type']
        message = data['message']
        receiver = self.room_name.replace(self.scope['user'].id, '').replace('-', '')
        receiver = CustomUser.objects.get(id=int(receiver))
        sender = self.scope['user']

        # Store message.
        m = Message(sender=sender, receiver=receiver, text=message).save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': message_type,
                'message': message,
                'date': datetime.strftime(m.date, '%d.%m.%Y %H:%M:%S'),
                'sender': sender.id,
                'receiver': receiver.id
            }
        )


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        sender = event['sender']
        receiver = event['receiver']
        date = event['date']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type,
            'date': date,
            'sender': sender,
            'receiver': receiver
        }))

    
    async def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        sender = event['sender']
        receiver = event['receiver']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type,
            'date': date,
            'sender': sender,
            'receiver': receiver
        }))