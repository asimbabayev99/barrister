from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/account/login')
def index(request, user_id):

    room_name = str(min(request.user.id, user_id)) + "-" + str(max(request.user.id, user_id))

    context = {
        'room_name': room_name,
    }

    return render(request, 'chat/index.html', context)