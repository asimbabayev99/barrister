from django.shortcuts import render,HttpResponse ,get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.



def shop_view(request, category=None):

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    else:
        basket = []

    categories = Category.objects.all()

    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except:
        page = 1
    
    if category:
        products = Product.objects.filter(category__slug=category)
    else:
        products = Product.objects.all()
    products.order_by('-id')

    paginator = Paginator(products, 24)
    page_obj = paginator.get_page(page)  

    context = {
        'product_count': paginator.count,
        'page_obj': page_obj,
        'basket':basket,
        'categories': categories,
        'basket_count': len(basket)
    }

    return render(request, 'shop/shop.html', context=context)


@login_required(login_url='/account/login')
def shop_basket_view(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related('product').order_by('-date')
    else:
        basket = []
    
    context = { 
        'basket_items':basket,
        'basket_count': len(basket)
    }


    return render(request,'shop/basket.html',context)

def product_single_view(request, id=None):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    else:
        basket = []

    if id:
        product = get_object_or_404(Product, id=id)
    else:
        product = Product.objects.all()  

    context = {
        'product': product,
        'basket': basket,
        'basket_count': len(basket)
    }       



    return render(request,'shop/product-single.html', context=context)
