from django.shortcuts import render,HttpResponse ,get_object_or_404, redirect
from .models import *
# Create your views here.


def index(request):

    return render(request, 'laws/index.html')


def codes(request):
    codes = Code.objects.all().order_by('number').values('id', 'number', 'name', 'active')
    
    context = {
        'codes': codes
    }
    return render(request, 'laws/codes.html', context=context)


def code_single(request, id):
    code = get_object_or_404(Code.objects.all(), id=id)

    context = {
        'code': code
    }

    return render(request, 'laws/code.html', context=context)