from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/account/login')
def index_view(request):
    
    return render(request,'clients/index.html')