from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *

def index_view(request):
    users = CustomUser.objects.filter(role="Barrister")[:4]
    profiles = []
    for user in users:
        profiles.append(Profile.objects.get(user=user))
    



    return render(request,"index.html",context={'profiles':profiles})

def single_view(request):
    return render(request,"barrister_single.html",context={})



@login_required(login_url='account/login')
def calendar_view(request):

    return render(request, "calendar.html", context={})