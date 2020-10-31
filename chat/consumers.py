from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from account.models import CustomUser
from chat.models import Message, Attachment
from datetime import datetime
from channels.db import database_sync_to_async
import base64
import json
import os
import uuid
from django.conf import settings


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
    upload_file = data.get('file')
    attachment = Attachment(message_id=message_id, name=name)
    attachment.save()
    attachment.file.save(name, File(upload_file))

    attachment.save()
    return attachment


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
        message_type = data.get('type')
        action = data.get('action')

        receiver = self.room_name.replace(str(self.scope['user'].id), '').replace('-', '')
        receiver = CustomUser.objects.get(id=int(receiver))
        sender = self.scope['user']

        # if message type is text
        if message_type == 'text':
            if action == 'post':
                message = data['message']
                # Store message.
                msg = await save_message(message=message, sender=sender.id, receiver=receiver.id)
            elif action == "delete":
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
                    'action': action,
                    'id': msg.id,
                    'message': message,
                    'date': datetime.strftime(msg.date, '%d.%m.%Y %H:%M:%S'),
                    'sender': sender.id,
                    'receiver': receiver.id
                }
            )
        # if message type is file
        elif message_type == "file" or True:
            if action == "prepare":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'handle_json',
                        'sender': sender,
                        'receiver': receiver,
                        'file_name': data.get('file_name'),
                        'file_size': data.get('file_size'),
                    }
                )
            elif action == "progress" or True:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'handle_chunk',
                        'file_size': data.get('file_size'),
                        'sender': sender,
                        'receiver': receiver,
                        'data': data.get('data'),
                    }
                )
            elif action == "post":
                pass
        else: 
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'handle_error',
                    'error_message': 'Exception. message_action  be one of these: text, file'
                }
            )


    async def handle_json(self, event):
        sender = event['sender']
        receiver = event['receiver']

        # filename and size of uploading file
        filename = event['file_name']
        size = event['file_size']

        # create file with uuid1 name in media/chat/attachments/ path
        name, extension = os.path.splitext(filename)
        path = os.path.join(settings.MEDIA_ROOT, 'chat', 'attachments', str(uuid.uuid1()) + extension)
        f = open(path, 'wb')

        # save temporaly file in session
        self.session = {
            'filename': filename,
            'upload_size': size,
            'upload_file': f,
            'sender': sender,
            'receiver': receiver,
            'path': path,
        }

        # inform user to send file data
        await self.send(text_data=json.dumps({
            'success': True,
            'action': 'progress',
            'file_size': 0,
        }))

                

    async def handle_chunk(self, event):
        # print("handle_chunk")
        data = event['data']
        sender = event['sender']
        receiver = event['receiver']

        base64_bytes = data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)

        upload_size = self.session.get('upload_size')
        temp_destination = self.session.get('upload_file')

        if not temp_destination:
            return self.error('Invalid request. Please try again.')
        
        self.session['upload_file'].write(message_bytes)
        size = self.session['upload_file'].tell()

        percent = round((size / upload_size) * 100)

        await self.send(text_data=json.dumps({
            'action': 'progress',
            'percent': percent,
            'file_size': size
        }))

        if size >= upload_size:
            # self.session['upload_file'].flush()
            self.session['upload_file'].close()
            filename = self.session['filename']
            msg = await save_message(sender=sender, receiver=receiver, message='')
            attch = await save_attachment(message_id=msg.id, name=filename, file=self.session['upload_file'])
            print("created")
            print("-"*50)
            # file_name = await self.handle_complete(self.session['upload_file'])

            # await self.send(text_data=json.dumps({
            #     'action': 'complete',
            #     'file_size': size,
            #     'file_name': file_name
            # }, close=True))
        
    
    async def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        sender = event['sender']
        action = event['action']
        receiver = event['receiver']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'success': True,
            'message': message,
            'type': message_type,
            'action': action,
            'date': date,
            'sender': sender.id,
            'receiver': receiver.id
        }))

    
    async def handle_error(self, event):
        error_message = event['error_message']

        await self.send(text_data=json.dumps({
            'success': 'False',
            'error_message': error_message,
        }))