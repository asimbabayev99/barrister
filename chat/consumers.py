from asgiref.sync import async_to_sync , sync_to_async
from django.core.files import File
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from account.models import CustomUser
from chat.models import Message, Attachment, Channel
from datetime import datetime
from channels.db import database_sync_to_async
import base64
import json
import os
import uuid
from home.models import *
from clients.models import *
# from channels.layers import get_channel_layer

    



@database_sync_to_async
def save_message(**data):
    message = data.get('message')
    sender = data.get('sender')
    receiver = data.get('receiver')
    viewed = data.get('viewed')
    msg = Message(sender=sender, receiver=receiver, text=message,viewed=viewed)
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
    original_name =  data.get('original_name')
    filename = data.get('filename')
    path = data.get('path')
    upload_file = open(path, 'rb')
    
    attachment = Attachment(message_id=message_id, name=original_name)
    attachment.file.name = path.replace(settings.MEDIA_ROOT, '') 
    attachment.save()

    attachment.save()
    return attachment

@database_sync_to_async
def save_channel(**data):
    user = data.get('user')
    channel = data.get('channel_name')
    channel = Channel(user_id=user.id,channel_name=channel)
    print(channel)
    channel.save()
    return Channel

@database_sync_to_async
def delete_channel(**data):
    user = data.get('user')
    channel = data.get('channel_name')

    Channel.objects.filter(user=user,channel_name=channel).delete()
    print('channel deleted')
    return 'deleted'

@database_sync_to_async
def update_messages(**data):
    try:
        last_message_id =data.get('id')
        sender = data.get('sender')
        receiver = data.get('receriver')
        messages = Message.objects.filter(sender_id=sender,receiver_id=receiver,id__lte=last_message_id,viewed=False)
        for i in messages:
            i.viewed = True
            i.save()
        return True
    except:
        return False


from django.db.models import Q
@database_sync_to_async
def get_users_channels(**data):
    user=data.get('user')
    print(user.role)
    if user.role is None or user.role.name == "User":
        users = Contact.objects.filter(user=user).values_list('barrister')
    else:
        if user.role.name == "Barrister":
            users = Contact.objects.filter(barrister=user).values_list('user')
        
    channels = list(Channel.objects.filter(user__in=users).select_related('user'))
    return channels

        

@database_sync_to_async
def get_channels(**data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    channels =  Channel.objects.filter(user__in=[sender,receiver])
    print(channels)
    return list(channels)



# @sync_to_async
# def send_message(**data):
#     obj = data.get('obj')
#     channels = data.get('channels')
#     print(channels)
#     message_type = data.get('message_type')
#     message = data.get('message')
#     action = data.get('action')
#     msg = data.get('msg')
#     sender = data.get('sender')
#     receiver = data.get('receiver')
#     for channel in channels:
#         obj.channel_layer.send(channel.channel_name,
#         {
#             'type': 'chat_message',
#             'message_type': message_type,
#             'action': action,
#             'id': msg.id,
#             'message': message,
#             'date': datetime.strftime(msg.date, '%d.%m.%Y %H:%M:%S'),
#             'sender': sender,
#             'receiver': receiver

#         })




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await save_channel(user=self.scope['user'],channel_name = self.channel_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name

        )
        user_channels = await get_users_channels(user=self.scope['user'])
        for channel in user_channels:

            await self.channel_layer.send(
                    channel.channel_name,
                        {
                        'type': 'status_message',
                        "user":self.scope['user'].id,
                        "status":'online'
                    }
                )
        await self.accept()

    async def disconnect(self, close_code):
        await delete_channel(user=self.scope['user'],channel_name = self.channel_name)
        user_channels = await get_users_channels(user=self.scope['user'])
        for channel in user_channels:
            await self.channel_layer.send(
                    channel.channel_name,
                        {
                        'type': 'status_message',
                        "user":self.scope['user'].id,
                        "status":'offline'
                    }
                )
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

        receiver = data.get('receiver')
        receiver = await database_sync_to_async(CustomUser.objects.get)(id = int(receiver))
        sender = self.scope['user']
        channels = await get_channels(receiver=receiver,sender=sender)
        
        # if message type is text
        if message_type == 'text':
            if action == 'post':
                message = data['message']
                viewed = False
                # Store message.
                msg = await save_message(message=message, sender=sender, receiver=receiver,viewed=False)
                for channel in channels:
                    await self.channel_layer.send()

            elif action == 'put':
                msg_id = data.get('id')
                sender = data.get('sender')
                
                viewed = await update_messages(sender=sender,receicer=receiver,id=msg_id)
                if viewed:
                    for channel in channels:
                        self.channel_layer.send(
                            channel.channel_name,
                            {
                            "type":'update_message',
                            "sender":sender,
                            "receiver":receiver,
                            "status":"readed"
                        })
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type':'handle_error',
                            'error_message':'mesajlarin oxunmasinda xeta bas verdi'
                        }
                    )

                

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

            
            
            for channel in channels:
                await self.channel_layer.send(
                    channel.channel_name,
                        {
                        'type': 'chat_message',
                        'message_type': message_type,
                        'action': action,
                        'id': msg.id,
                        'message': message,
                        'date': datetime.strftime(msg.date, '%d.%m.%Y %H:%M:%S'),
                        'sender': sender,
                        'receiver': receiver,
                        'viewed':viewed
                    }
                )
        

        # if message type is file
        elif message_type == "file":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_file_message',
                    'action': action,
                    'id': data['id'],
                    'message': data['message'],
                    'filename': data['filename'],
                    'url': data['url'],
                    'date': data['date'],
                    'sender': sender,
                    'receiver': receiver
                }
            )
            # if action == "prepare":
            #     channel_layer = get_channel_layer()
            #     await channel_layer.send(self.channel_name, {
            #         'type': 'handle_json',
            #         'sender': sender,
            #         'receiver': receiver,
            #         'file_name': data.get('file_name'),
            #         'file_size': data.get('file_size'),
            #     })
                
            # elif action == "progress":
            #     channel_layer = get_channel_layer()
            #     await channel_layer.send(self.channel_name, {
            #         'type': 'handle_chunk',
            #         'file_size': data.get('file_size'),
            #         'sender': sender,
            #         'receiver': receiver,
            #         'data': data.get('data'),
            #     })
        else: 
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'handle_error',
                    'error_message': 'Message action should be one of these: text, file'
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
        name = str(uuid.uuid1()) + extension
        path = os.path.join(settings.MEDIA_ROOT, 'chat', 'attachments', name)
        f = open(path, 'wb')

        # save temporaly file in session
        self.session = {
            'original_name': filename,
            'filename': name,
            'upload_size': size,
            'upload_file': f,
            'sender': sender,
            'receiver': receiver,
            'path': path,
        }

        # inform user to send file data
        await self.send(text_data=json.dumps({
            'success': True,
            'type': 'file',
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

        
        if size < upload_size:
            await self.send(text_data=json.dumps({
                'success': True,
                'type': 'file',
                'action': 'progress',
                'percent': percent,
                'file_size': size
            }))
        else:
            # self.session['upload_file'].flush()
            original_name = self.session['original_name']
            filename = self.session['filename']
            self.session['upload_file'].close()

            # save attachment
            msg = await save_message(sender=sender, receiver=receiver, message='')
            attch = await save_attachment(message_id=msg.id, filename=filename, original_name=original_name, path=self.session['path'])

            # print("created")
            # print("-"*50)

            await self.send(text_data=json.dumps({
                'success': True,
                'message': msg.text,
                'type': 'file',
                'action': 'complete',
                'date': str(attch.date),
                'file_size': size,
                'filename': original_name,
                'file_link': attch.file.url,
                'sender': sender.id,
                'receiver': receiver.id,
            }))
        
    
    async def chat_message(self, event):

        message = event['message']
        # message_type = event['type']
        sender = event['sender']
        action = event['action']
        receiver = event['receiver']
        date = event['date']
        viewed = event['viewed']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'success': True,
            'message': message,
            'type': 'text',
            'action': action,
            'date': date,
            'sender': sender.id,
            'receiver': receiver.id,
            'viewed':viewed
        }))

    async def status_message(self,event):
        user=event['user']
        status=event['status']
        print(user)
        await self.send(text_data=json.dumps({
            "type":'status_message',
            "user":user,
            "status":status
        }))



    async def chat_file_message(self, event):
        id = event['id']
        action = event['action']
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        filename = event['filename']
        url = event['url']
        date = event['date']

        await self.send(text_data=json.dumps({
            'success': True,
            'action': action,
            'id': id,
            'message': message,
            'type': 'file',
            'filename': filename,
            'sender': sender.id,
            'receiver': receiver.id,
            'url': url,
            'date': date
        }))

    
    async def handle_error(self, event):
        error_message = event['error_message']

        await self.send(text_data=json.dumps({
            'success': 'False',
            'error_message': error_message,
        }))
    
    async def update_message(self,event):
        user = event['user']
        status = event['status']
        await self.send(text_data=json.dumps({
            'type':'message_status',
            'user':user,
            'status':status

        }))
