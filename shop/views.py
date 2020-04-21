from django.shortcuts import render,HttpResponse ,get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.



def shop_view(request):


    return render(request, 'shop/shop.html', context={})