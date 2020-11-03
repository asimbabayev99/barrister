from django.shortcuts import render,HttpResponse ,get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *
from account.forms import UserForm, UserUpdateForm, ProfileUpdateForm
from home.forms import * 
from django.utils.text import slugify
from .models import News
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext as _
from shop.models import Basket
import smtplib,ssl,base64
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart,MIMEBase
from django.views.decorators.clickjacking import xframe_options_exempt
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from email.mime.application import MIMEApplication
from os.path import basename , realpath
from django.core.mail import send_mail
from account.tasks import synchronize_mail
import re
import os



def index_view(request):
    barristers = CustomUser.objects.filter(role__name='Barrister').prefetch_related('profile', 'profile__job_category').order_by('-id')[:4]
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
def calendar_events(request):
    categories = EventCategory.objects.all()

    context = {
        'categories': categories
    }

    return render(request, "calendar-events.html", context=context)



@login_required(login_url='/account/login')
def calendar(request):
    categories = EventCategory.objects.all()

    context = { 
        'categories': categories,
        'statuses': APPOINTMENT_STATUSES,
    }
    return render(request, 'calendar.html', context=context)






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




@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
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


@login_required(login_url='/account/login')
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
    

@login_required(login_url='/account/login')
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
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # if request.POST.get('image-clear'):
            #     print("clear image")
            #     form.image = None
            form.save()

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

 


from account.tasks import get_last_mails
@login_required(login_url='/account/login')
@xframe_options_exempt
def email_view(request, folder=None):
    email_acc , created = EmailAccount.objects.get_or_create(user=request.user)
    # get_last_mails.delay(email_acc.email,email_acc.token)
    emails = Email.objects.filter(user=request.user, folder=folder).order_by('-date').values(
         'subject','sender', 'receiver', 'date', 'flag')
    page = request.GET.get('page')
    try:
        page = int(page)
    except: 
        page = 1

    paginator = Paginator(emails, 50)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'barrister/email.html', context=context)
    



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



from barrister.settings import STATIC_ROOT , MEDIA_ROOT
@login_required(login_url='account/login')
def send_email(request):
    if request.method == "POST":
        try:
            email_account = EmailAccount.objects.get(user=request.user)
        except:
            return Http404

        if email_account.token is None:
            return redirect('https://oauth.yandex.com/authorize?response_type=token&client_id=7752b555854248a7b17a4800a475d157')
        email = email_account.email
        access_token = email_account.token
        message = "user={0}\@yandex.ru\001auth=Bearer {1}\001\001".format(email, access_token)
        message_bytes = message.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_string = base64_bytes.decode('utf-8')
        smtp_conn = smtplib.SMTP('smtp.yandex.com', 587)
        smtp_conn.set_debuglevel(False)
        smtp_conn.ehlo('test')
        smtp_conn.starttls()
        smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64_string)
        msg = MIMEMultipart()
        msg.attach(MIMEText(request.POST.get('content'),'plain'))
        msg.add_header('From',email)
        msg.add_header('Subject',request.POST.get('subject'))
        msg.add_header('To',request.POST.get('receiver'))
        msg.add_header('Cc',request.POST.get('cc'))
        msg.add_header('Bcc',request.POST.get('bcc') )
        if 'image' in request.FILES:
            for img in request.FILES.getlist('image'):
                image = MIMEImage(img.read(),basename="{0}".format(img.name), _subtype=re.sub('image/',"",img.content_type))
                image.add_header('Content-Disposition', 'attachment; filename={0}'.format(img.name))
                msg.attach(image)
        if 'file' in request.FILES:
            for fayl in request.FILES.getlist('file'):
                part = MIMEApplication(fayl.read(),basename=fayl.name,_subtype=re.sub('application/',"",fayl.content_type))
                part['Content-Disposition'] = 'attachment; filename="{0}"'.format(fayl.name)
                msg.attach(part)
        smtp_conn.sendmail(email,request.POST.get('receiver'),msg.as_string())
        smtp_conn.close()
        
    return render(request, 'barrister/send_email.html')






# def attachment_media_access(request, path):
#     """
#     When trying to access :
#     myproject.com/media/uploads/passport.png

#     If access is authorized, the request will be redirected to
#     myproject.com/protected/media/uploads/passport.png

#     This special URL will be handle by nginx we the help of X-Accel
#     """

#     access_granted = False

#     user = request.user
#     if user.is_authenticated():
#         if user.is_staff:
#             # If admin, everything is granted
#             access_granted = True
#         else:
#             # For simple user, only their documents can be accessed
#             user_documents = [
#                 # add here more allowed documents
#             ]

#             for doc in user_documents:
#                 if path == doc.name:
#                     access_granted = True

#     if access_granted:
#         response = HttpResponse()
#         # Content-type will be detected by nginx
#         del response['Content-Type']
#         response['X-Accel-Redirect'] = '/protected/media/' + path
#         return response
#     else:
#         return HttpResponseForbidden('Not authorized to access this media.')

def social_activity_list(request):
    publications = Publication.objects.all().order_by('date')
    paginator = Paginator(publications,7)
    page_number = request.GET.get('page')
    try:
        publications = paginator.get_page(page_number)
    except:
        publications = paginator.get_page(1)
    
    context = {'publications':publications}
    return render(request,'socialActivity.html',context=context)



def mail_content_view(request):

    return render(request,'mailContent.html')




#check file is image or not for content-type in response
from PIL import Image
def is_image(file_path):
    try:
        i = Image.open(file_path)
        return True

    except:
        return False


import magic
from home.models import Attachment
import mimetypes

def attachment_media_download(request,path):
    path='media/'+path
    print(path)
    file_name = os.path.basename(path)
    if os.path.exists(path):
        with open(path,'rb') as fayl:
            response = HttpResponse(fayl.read(),content_type='{}'.format(magic.from_file(path,mime=True)))
            response['Content-type']  = mimetypes.guess_type(path)
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response
    raise Http404


@xframe_options_exempt
def attachment_media_view(request,path):
   
    if os.path.exists(path):
        file_name = os.path.basename(path)
        print(file_name)
        with open(path,'rb') as fayl:
            response = HttpResponse(fayl.read(),content_type=mimetypes.guess_type(path)[0])
            response['Content-type']  = mimetypes.guess_type(path)[0]
            response["Content-Disposition"] = "filename={}".format(file_name) 
            return response
    return Http404


def viewer_test(request):
    return render(request,'docx_viewer.html')    


def email_draft(request):
    return render(request,'email_draft.html')

def email_trash(request):
    return render(request,'email_trash.html')
    