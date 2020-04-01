from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import *
from account.models import *

def index_view(request):
    profiles = Profile.objects.filter(user__role__name='Barrister').order_by('-id')[:4]
    print(profiles)

    return render(request, "index_test.html", context={'profiles':profiles})



def single_view(request, id):
    profile = Profile.objects.get(id=id)
    skills = Skill.objects.filter(profile=profile)

    context = {
        "profile": profile,
        "skills": skills,
    }
    return render(request, "barrister_single.html", context=context)



@login_required(login_url='account/login')
def calendar_view(request):

    return render(request, "calendar.html", context={})