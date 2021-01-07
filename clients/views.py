from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse , Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt , xframe_options_deny
from .models import *
import os
import mimetypes

@login_required(login_url='/account/login')
def index(request):
    active_clients = Client.objects.filter(barrister=request.user).filter(status='active')
    inactive_clients = Client.objects.filter(barrister=request.user).filter(status='inactive')
    context = {
        'active_clients': active_clients,
        'inactive_clients':inactive_clients
    }
    return render(request,'clients/index.html',context=context)

@login_required(login_url = "/account/login")
def client_documents(request,id):
    client = get_object_or_404(Client.objects.all(),pk=id)
    cases = client.case.all().order_by('-id')
    appointments = client.contact.appointments.all()
    notes = Notes.objects.filter(barrister=request.user,client_id=id)
    context={'cases':cases,"client_id":id,"notes":notes,'appointments':appointments}
    return render(request,"clients/documents.html",context=context)

def case_document_download(request,path):
    file_name  = os.path.basename(path)
    if os.path.exists(path):
        with open(path,"wb+") as document:
            response = HttpResponse(document.read(),content_type=mimetypes.guess_type(path)[0])
            response['Content-type']  = mimetypes.guess_type(path)[0]
            response["Content-Disposition"] = "filename={}".format(file_name) 
            return response
    return Http404

# @xframe_options_deny
def document_viewer(request):
    return render(request, 'clients/viewer.html')