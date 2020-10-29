from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from account.models import CustomUser
from chat.models import Message, Attachment
from datetime import datetime
from channels.db import database_sync_to_async


@database_sync_to_async
def save_message(**data):
    message = data.get('message')
    sender = data.get('sender')
    receiver = data.get('receiver')
    # Store message.
    msg = Message(sender=sender, receiver=receiver, text=message)
    msg.save()
    return msg


@database_sync_to_async
def delete_message(**data):
    id = data.get('id')
    try:
        msg = Message.objects.get(id=id)
    except:
        return False
    if msg.sender == data.get('sender') and msg.receiver == data.get('receiver'):
        msg.delete()
        return True
    else:
        return False
    

@database_sync_to_async
def save_attachment(**data):
    message_id = data.get('message_id')
    name = data.get('name')
    upload_file = data.get('upload_file')
    # attachment = Attachment(message_id=message_id, file=upload_file)
    # return attachment


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print("connect")
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
        data = json.loads(text_data)
        message_type = data.get('message_type')
        message_action = data.get('message_action')

        receiver = self.room_name.replace(str(self.scope['user'].id), '').replace('-', '')
        receiver = CustomUser.objects.get(id=int(receiver))
        sender = self.scope['user']

        # if message type is text
        if message_type == 'text':
            if message_action == 'post':
                message = data['message']
                # Store message.
                msg = await save_message(message=message, sender=sender, receiver=receiver)
            elif message_action == "delete":
                message = ""
                id = data['id']
                result = await delete_message(id=id, sender=sender, receiver=receiver)
                if not result:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'handle_error',
                            'error_message': 'Exception occured during deleting message'
                        }
                    )   
            else:
                # if wrong message action is wrong then send error message
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'handle_error',
                        'error_message': 'Exception. message_type action be one of these: post, delete'
                    }
                )

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_type': message_type,
                    'message_action': message_action,
                    'id': msg.id,
                    'message': message,
                    'date': datetime.strftime(msg.date, '%d.%m.%Y %H:%M:%S'),
                    'sender': sender.id,
                    'receiver': receiver.id
                }
            )
        # if message type is file
        elif message_type == "file":
            if message_action == "post":
                self.session = {
                    # Set up file object and attributes
                    'upload_file': '',
                    'name': '',
                    'size': ''
                }

            elif message_action == "delete":
                pass
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'handle_error',
                        'error_message': 'Exception. message_type be one of these: post, delete'
                    }
                )
        else: 
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'handle_error',
                    'error_message': 'Exception. message_action  be one of these: text, file'
                }
            )
                

    async def handle_chunk(self, message, **kwargs):
        upload_size = self.session.get('upload_size')
        temp_destination = self.session.get('upload_file')

        if not upload_size or not temp_destination:
            return self.error('Invalid request. Please try again.')

        self.session['upload_file'].write(message)
        size = self.session['upload_file'].tell()

        percent = round((size / upload_size) * 100)
        await self.send_json({
            'action': 'progress',
            'percent': percent,
            'file_size': size
        })

        if size >= upload_size:
            self.session['upload_file'].flush()
            file_name = await self.handle_complete(self.session['upload_file'])

            await self.send_json({
                'action': 'complete',
                'file_size': size,
                'file_name': file_name
            }, close=True)
        
    
    async def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        sender = event['sender']
        receiver = event['receiver']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'success': True,
            'message': message,
            'message_type': message_type,
            'date': date,
            'sender': sender,
            'receiver': receiver
        }))

    
    async def handle_error(self, event):
        error_message = event['error_message']

        await self.send(text_data=json.dumps({
            'success': 'False',
            'error_message': error_message,
        }))