from django.shortcuts import render,HttpResponse ,get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *
from account.forms import UserForm, UserUpdateForm, ProfileUpdateForm
from home.forms import * 
from django.utils.text import slugify
from .models import News
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext as _
from shop.models import Basket



def index_view(request):
    barristers = CustomUser.objects.filter(role__name='Barrister').prefetch_related('profile', 'profile__job_category').order_by('-id')[:4]
    # print(profiles)
    
    news = News.objects.all().order_by('-date')[:5]
    news = news.values('title', 'date', 'image', 'slug')
    
    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = {
        'barristers': barristers,
        'news': news,
        'basket_count': basket_count,
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

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = {
        "profile": profile,
        "skills": skills,
        "experiences": experiences,
        "awards": awards,
        "basket_count": basket_count,
    }
    return render(request, "barrister_single.html", context=context)




@login_required(login_url='/account/login')
def calendar_view(request):


    return render(request, "calendar-date.html", context={})




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

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = {
        'barristers': barristers,
        'basket_count': basket_count,
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
    


def admin_news_update(request,slug):
    if request.user.is_superuser is False:
        return Http404()
        
    news = get_object_or_404(News, slug=slug)
    form = Newsform(instance=news)
    if request.method == "POST":
        form = Newsform(request.POST,request.FILES,instance=news)
        if form.is_valid():
            news.date = timezone.now()
            news.title = form.cleaned_data['title']
            news.content = form.cleaned_data['content']
            news.image = form.cleaned_data['image']
            news.save()
            return redirect('admin-news-list')
            

    form = Newsform(instance=news)
    return render(request,'admin-panel/admin-UpdateNews.html',context={'form':form})



def blog_grid_view(request):

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = {
        'basket_count': basket_count,
    }

    return render(request, 'blog-grid-view.html', context=context)



def blog_large_view(request):

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = { 
        'basket_count': basket_count,
    }

    return render(request,'blog-large-image.html', context=context)



def blog_single_view(request):

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = { 
        "basket_count": basket_count,
    }

    return render(request,'blog-single.html', context=context)



def contacts_view(request):

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = { 
        "basket_count": basket_count,
    }
    
    return render(request,'contacts.html', context=context)




def attorneys_view(request):
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1


    attorneys = CustomUser.objects.filter(role__name='Barrister').prefetch_related('profile')
    paginator = Paginator(attorneys, 3)
    page_obj = paginator.get_page(page)

    # for i in page_obj:
    #     print(i)

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).count()
    else:
        basket_count = 0

    context = {
        "page_obj": page_obj,
        "basket_count": basket_count,
    }

    return render(request,'attorneys.html', context=context)



@login_required(login_url='/account/login')
def is_masasi(request):
    return render(request,'barrister/barrister-admin.html')



@login_required(login_url='/account/login')
def new_appointment_view(request):
    form = AppointmentForm()
    message = ""

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.user = request.user
            new_appointment.save()

            message = "Görüş uğurla elavə olundu"

    context = {
        'form' : form,
        'message': message,
    }

    return render(request,'barrister/new-appointment.html', context=context)    
      


@login_required(login_url='/account/login')
def add_task_view(request):
    form = TaskForm()
    message = ""

    if request.method == 'POST' :
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task = request.user
            new_task.save()
            message = "Tapşırıq uğurla əlavə olundu"
        else:
            print("invalid")
            print(form.errors)
    
    context = {
        'form': form,
        'message': message
    }
    
    return render(request, 'barrister/new-task.html', context=context)


@login_required(login_url='/account/login')
def barrister_account(request):
    form = UserUpdateForm(instance=request.user)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }      

    return render(request,'barrister/barrister-account.html', context=context)    

    

@login_required(login_url='/account/login')
def barrister_personal(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileUpdateForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # user.first_name = form.cleaned_data['first_name']
            # user.last_name = form.cleaned_data['last_name']
            # user.address = form.cleaned_data['address']
            # user.phone_number = form.cleaned_data['phone_number']
            # user.save()
            form.save()

    form = ProfileUpdateForm(instance=profile)
    context = {
        'form': form,
    }      

    return render(request,'barrister/barrister-personal.html', context=context)    



@login_required(login_url='/account/login')
def barrister_professional_skills(request):

    profile = request.user.profile
    experiences = EducationAndWorkExperience.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile)

    context = {
        "profile": profile,
        "experiences": experiences,
        "skills": skills,
    }

    return render(request, 'barrister/professional-skills.html', context=context)




@login_required(login_url='/account/login')
def barrister_current_tasks(request):
    status = request.GET.get('status')
    if status:
        tasks = Task.objects.filter(status=status)
    else:
        tasks = Task.objects.all()

    page = request.GET.get('page')
    try:
        page = int(page)
    except: 
        page = 1


    paginator = Paginator(tasks, 20)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'barrister/current_task.html', context=context)




@login_required(login_url='/account/login')
def barrister_completed_tasks(request):
    status = request.GET.get('status')
    if status:
        tasks = Task.objects.filter(status=status)
    else:
        tasks = Task.objects.all()

    page = request.GET.get('page')
    try:
        page = int(page)
    except: 
        page = 1


    paginator = Paginator(tasks, 20)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'barrister/completed_task.html', context=context)

 



@login_required(login_url='/account/login')
def email_view(request, folder=None):
    if folder:
        email_list = Folder.objects.filter(name=folder, user=request.user).select_related('email')
    else:
        email_list = Folder.objects.filter(name="Inbox", user=request.user).select_related('email')

    page = request.GET.get('page')
    try:
        page = int(page)
    except: 
        page = 1

    paginator = Paginator(email_list, 50)
    page_obj = paginator.get_page(page)


    context = {
        'page_obj': page_obj
    }

    return render(request, 'barrister/email.html', context=context)




@login_required(login_url='/account/login')
def single_email_view(request, email_id):
    email = get_object_or_404(Email.objects.all(), id=email_id)
    if email.sender != request.user and email.receiver != request.user:
        raise Http404()

    context = {
        'email': email
    }

    return render(request, '', context=context)


@login_required(login_url='/account/login')
def move_mail_to_folder(request, email_id):
    email = get_object_or_404(Email.object.all(), id=email_id)

    if request.method == "POST":
        old_folder = request.POST.get('old_folder')
        new_folder = request.POST.get('new_folder')

        if old_folder and new_folder:
            folder = Folder.objects.get(folder=folder)
            folder.email.remove(email)
            folder = Folder.objcets.get(folder=folder)
            folder.email.add(email)
            folder.save()

            return JsonResonse({"detail": "Email moved to {0} folder".format(new_folder)}, status=201)
        else:
            return JsonReponse({"detail": "Bad request"}, status=400)

    else:
        return JsonReponse({"detail": "Bad request"}, status=400)



@login_required(login_url='account/login')
def remove_email(request, email_id):
    email = get_object_or_404(Email.objects.all(), id=email_id)
    if email.sender != request.user and email.receiver != request.user:
        return Http404()

    folder = Folder.objects.filter(name="Deleted", user=request.user)
    folder.remove(email)
    email.delete()

    return JsonResponse({"detail": "email deleted"}, status=201)




@login_required(login_url='account/login')
def send_email(request):


    return render(request, 'barrister/send_email.html')