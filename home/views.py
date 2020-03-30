from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index_view(request):
    
    return render(request,"index.html",context={})



@login_required(login_url='account/login')
def calendar_view(request):

    return render(request, "calendar.html", context={})