from django.shortcuts import render,HttpResponse ,get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *
from account.forms import UserForm
from home.forms import * 
from django.utils.text import slugify
from .models import News
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext as _



def index_view(request):
    barristers = CustomUser.objects.filter(role__name='Barrister').prefetch_related('profile', 'profile__job_category').order_by('-id')[:4]
    # print(profiles)
    
    news = News.objects.all().order_by('-date')[:5]
    news = news.values('title', 'date', 'image', 'slug')

    context = {
        'barristers': barristers,
        'news': news
    }
    return render(request, "index.html", context=context)




def single_view(request, id):
    user = get_object_or_404(CustomUser.objects.all().select_related('role'), id=id)
    if user.role is None or user.role.name != 'Barrister':
        raise Http404()

    profile, created = Profile.objects.get_or_create(user=user)
    skills = Skill.objects.filter(profile=profile)
    experiences = EducationAndWorkExperience.objects.filter(profile=profile)
    awards = Award.objects.filter(profile=profile)

    context = {
        "profile": profile,
        "skills": skills,
        "experiences": experiences,
        "awards": awards,
    }
    return render(request, "barrister_single.html", context=context)




@login_required(login_url='/account/login')
def calendar_view(request):


    return render(request, "calendar-date.html", context={})




def news_add_view(request):
    if request.user.role != "Barrister":
        return HttpResponse('<p>Permission denied</p>')

    errors = {}
    form = Newsform()
    if request.user.is_staff is False:
        return Http404()

    if request.method == "POST":
        form = Newsform(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            user = request.user 
            slug = slugify(title)
            news = News(title=title,content=content,image=image,user = user, slug=slug)
            news.save()   
        else:
            errors['message'] = 'Form is not valid'
        form = Newsform()
    
    context = {
        'form': form,
        'errors': errors,
    }
    return render(request, 'news_add.html', context=context)




def admin_news_update(request,slug):
    if request.user.is_superuser is False:
        return Http404()
        
    news = get_object_or_404(News.objects.all(),slug=slug)
    form = Newsform(instance=news)
    if request.method == "POST":
        form = Newsform(request.POST,request.FILES,instance=news)
        if form.is_valid():
            news.title = form.cleaned_data['title']
            news.content = form.cleaned_data['content']
            news.image = form.cleaned_data['image']
            news.save()
            

    form = Newsform(instance=news)
    return render(request,'admin-panel/admin-UpdateNews.html',context={'form':form})




def news_view(request):
    news = News.objects.all()
    
    context = {
        "news":news
    }
    return render(request, "news.html", context=context)




def news_detail_view(request, slug):
    news = get_object_or_404(News, slug = slug)
    context = {
        'news': news
    }
    return render(request, "news_detail.html", context=context)
        




def publication_add_view(request):

    form = PublicationForm()
    # if request.user.role is None or  request.user.role.name is not "Barrister":
    #     raise Http404()

    if request.method == "POST":
        form = PublicationForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = Publication(**form.cleaned_data)
            new_post.user = request.user
            new_post.save()


    context = {
        'form': form,
    }

    return render(request, 'xeber_elave_etmek_user_ucun.html', context=context)



def publication_show_view(request):   
    
    publications = Publication.objects.all().order_by("-date")[:10]
    context = {
        "publications":publications
    }
    return render(request, context=context)



def about_us_view(request):

    barristers = CustomUser.objects.filter(role__name='Barrister').prefetch_related('profile', 'profile__job_category')
    # for i in barristers:
    #     print(i.profile.job_category)

    context = {
        'barristers': barristers,
    }

    return render(request,'about-us.html',context=context)





def admin_user_list(request):

    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1
 
    users = CustomUser.objects.all().select_related('role').order_by('-id')
    paginator = Paginator(users, 2)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'admin-panel/admin-UserList.html', context=context)



def admin_user_add(request):

    message = None
    form = UserForm()

    if request.method == "POST": 
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            image = request.FILES.get('image', None)

            user = CustomUser(
                first_name=first_name, 
                last_name=last_name, 
                middle_name=middle_name,
                email=email, 
                role=role
            )
            user.password = make_password(password)
            user.save()

            profile = Profile(
                user=user,
                image=image,
            ).save()
            
            form = UserForm()
            message = 'İstifadəçi uğurla əlavə olundu'

    context = {
        'form':form,
        'message': message,
    }
    return render(request, 'admin-panel/admin-AddUser.html', context=context)



def admin_add_news(request):

    form = Newsform()
    if request.method == 'POST' :

        form = Newsform(request.POST,request.FILES or None)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            news = News(title=title,content=content,image=image,user=request.user)
            news.save()
    form = Newsform()
    
    return render(request,'admin-panel/admin-AddNews.html',context={ 'form':form})



def admin_news_list(request):

    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1

    news = News.objects.all().order_by("-date")
    paginator = Paginator(news, 4)
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
    }


    return render(request, 'admin-panel/admin_NewsList.html', context = context)
    


def blog_grid_view(request):

    return render(request, 'blog-grid-view.html')

def blog_large_view(request):
    return render(request,'blog-large-image.html')

def blog_single_view(request):
    return render(request,'blog-single.html')

def contacts_view(request):
    return render(request,'contacts.html')

def shop_view(request):
    return render(request,'shop/shop.html')

def shop_basket_view(request):
    return render(request,'shop/basket.html')

def product_single_view(request):
    return render(request,'shop/product-single.html')


def get_tasks_list(request):

    status = request.GET.get('status')
    if status:
        tasks = Task.objects.filter(status=status)
    else:
        tasks = Task.objects.all()

    paginator = Paginator(tasks, 20)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, '', context=context)


def add_task_view(request):

    form = TaskForm()

    if request.method == 'POST' :
        form = TaskForm(request.POST, request.user)
        if form.is_valid():
            form.save()
    
    context = {
        'form': form,
    }
    
    return render(request, '', context=contetx)


