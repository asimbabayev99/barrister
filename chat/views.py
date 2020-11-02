from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from chat.models import Message, Attachment
from django.shortcuts import get_object_or_404
import os
import json
# Create your views here.


@login_required(login_url='/account/login')
def index(request, user_id):

    room_name = str(min(request.user.id, user_id)) + "-" + str(max(request.user.id, user_id))
    messages = Message.objects.filter(Q(sender=request.user) & Q(receiver_id=user_id) | Q(receiver=request.user) & Q(sender_id=user_id)).order_by('date')

    context = {
        'receiver': user_id,
        'messages': messages,
        'room_name': room_name,
    }

    return render(request, 'chat/index.html', context)




@login_required(login_url='/account/login')
def upload_file(request, user_id):

    if request.is_ajax():
        if request.method == 'POST':
            files = request.FILES
            attached_file = files.get('file')
            if not attached_file:
                return JsonResponse({
                    'detail': 'File not found'
                }, status=400)
            msg = Message(sender=request.user, receiver_id=user_id, text='')
            msg.save()
            attch = Attachment(message=msg, file=attached_file, name=attached_file.name)
            attch.save()
            return JsonResponse({
                'id': msg.id,
                'message': msg.text,
                'filename': attached_file.name,
                'url': attch.file.url,
                'date': attch.date,
            }, status=200)
        else:
            return JsonResponse({   
                   'detail': 'Bad request' 
            }, status=400)
    else:
        return JsonResponse({
            'detail': 'Bad request' 
        }, status=400)
