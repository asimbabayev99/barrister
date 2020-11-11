from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/account/login')
def index(request):
    return render(request,'clients/index.html')

# @login_required(login_url = "/account/login")
def client_documents(request):
    # Davay ala işdə
    return render(request,"clients/documents.html")