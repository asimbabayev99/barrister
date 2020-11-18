from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *


@login_required(login_url='/account/login')
def index(request):
    active_clients = Client.objects.filter(barrister=request.user).filter(status='active')
    inactive_clients = Client.objects.filter(barrister=request.user).filter(status='inactive')
    context = {
        'active_clients': active_clients,
        'inactive_clients':inactive_clients
    }
    return render(request,'clients/index.html',context=context)

# @login_required(login_url = "/account/login")
def client_documents(request,id):
    client = get_object_or_404(Client.objects.all(),pk=id)
    cases = client.case.all()
    return render(request,"clients/documents.html")