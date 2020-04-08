from django.shortcuts import render,HttpResponse ,get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *
from home.forms import Newsform 
from django.utils.text import slugify
from .models import News



def index_view(request):
    profiles = Profile.objects.filter(user__role__name='Barrister').order_by('-id')[:4]
    # print(profiles)
    news = News.objects.all().order_by('-date')[:5]
    news = news.values('title', 'date', 'image', 'slug')

    context = {
        'profiles': profiles,
        'news': news
    }
    return render(request, "index_test.html", context=context)




def single_view(request, id):
    if request.user.role.name is not "Barrister":
        raise Http404("Profile does not exist")
    profile = Profile.objects.get(id=id)
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




@login_required(login_url='account/login')
def calendar_view(request):


    return render(request, "calendar.html", context={})




def news_add_view(request):
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




def news_update(request,slug):
    if request.user.is_staff is False:
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
    return render(request,'news_update.html',context={'form':form})




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
    if request.user.role.name is not "Barrister":
        return Http404()

    if request.method == "POST":
        form = PublicationForm(request.POST,request.FILES,instance=news)
        if form.is_valid():
            new_post = Publication(**form.cleaned_data)
            new_post.user = request.user
            new_post.save()


    context = {
        'form': form,
    }

    return render(request, '', context=context)
