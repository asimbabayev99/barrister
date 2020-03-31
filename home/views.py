from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index_view(request):
    
    return render(request,"index.html",context={})

def single_view(request):
    return render(request,"barrister_single.html",context={})

@login_required(login_url='account/login')
def calendar_view(request):

    return render(request, "calendar.html", context={})