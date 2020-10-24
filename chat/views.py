from django.shortcuts import render

# Create your views here.

def index(request, user_id):

    room_name = str(min(request.user.id, user_id)) + "-" + str(max(request.user.id, user_id))

    context = {
        'room_name': room_name,
    }

    return render(request, 'chat/index.html', context)