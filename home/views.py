from django.shortcuts import render,HttpResponse ,get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *
from home.forms import Newsform 
from django.utils.text import slugify

def index_view(request):
    profiles = Profile.objects.filter(user__role__name='Barrister').order_by('-id')[:4]
    print(profiles)

    return render(request, "index_test.html", context={'profiles':profiles})



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
    if request.user.role != "Barrister":
        return HttpResponse('<p>Permission denied</p>')

    errors = {}
    form = Newsform()
    if request.method == "POST":
        form = Newsform(request.POST,request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            user = request.user 
            news = News(title=title,content=content,image=image,user = user)
            news.save()   
        else:
            errors['message'] = 'Error'
        form = Newsform()
    
    return render(request,'news_add.html',context={'form':form,'errors':errors})

def news_update(request,slug):

    if request.user.role != "Barrister":
        return HttpResponse('<h1>Permission denied</h1>')

    news = get_object_or_404(News.objects.all(),slug=slug)
    if request.user != news.user:
        return HttpResponse('<h1>Permission denied</h1>')
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


        
