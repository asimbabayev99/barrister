from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from chat.models import Message, Attachment
from django.shortcuts import get_object_or_404
# Create your views here.


@login_required(login_url='/account/login')
def index(request, user_id):

    room_name = str(min(request.user.id, user_id)) + "-" + str(max(request.user.id, user_id))
    messages = Message.objects.filter(Q(sender=request.user) & Q(receiver_id=user_id) | Q(receiver=request.user) & Q(sender_id=user_id)).order_by('date')

    context = {
        'messages': messages,
        'room_name': room_name,
    }

    return render(request, 'chat/index.html', context)