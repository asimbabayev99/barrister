from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from django.urls import reverse
from account.models import *
from account.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from home.forms import PublicationForm
from home.models import Publication



def login_view(request):
    form = LoginForm()
    errors = {}  # may contain authentication errors

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)

            next = request.GET.get('next')
            print(next)
            if next:
                return redirect(next)
            else: 
                return redirect(reverse('home'))
        else:
            errors['message'] = 'Email or password is invalid'


    context = {
        'errors': errors,
        'form': form,
    }

    return render(request, 'account/login.html', context=context)



def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            if 'confirm_password' in form.cleaned_data:
                del form.cleaned_data['confirm_password']

            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_user = CustomUser(**form.cleaned_data)
            # new_user = CustomUser(
            #     first_name=first_name, last_name=last_name, email=email
            # )
            new_user.password = make_password(password)
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()

            form = LoginForm()
            context = {
                'form': form
            }
            return render(request, 'account/login.html', context=context)

    context = {
        "form": form,
    }

    return render(request, 'account/register_test.html',context=context)




def logout_view(request):
    logout(request)
    return redirect(reverse('login'))



@login_required(login_url='/account/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('change-password'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change-password.html', {
        'form': form
    })    


def user_list_view(request):
    user_list = CustomUser.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 24)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer 
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "user-list.html", context=context)



def user_detail_view(request, pk):

    user = CustomUser.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    skills = Skill.objects.filter(profile=profile)
    awards = Award.objects.filter(profile=profile)
    experiences = EducationAndWorkExperience(profile=profile)

    context = {
        'user': user,
        'profile': profile,
        'skills': skills,
        'awards': awards,
        'experiences': experiences,
    }
    return render(request, 'user-detail.html', context=context)




@login_required(login_url='/account/login')
def user_profile(request):

    # return render(request, 'user-profile.html')
    return render(request, 'barrister/barrister-admin.html')


def advocat_user(request):
    if request.user.role.name != "Barrister":
        return HttpResponse('<h1>Permission denied</h1>')
    last_publications = Publication.objects.filter(user=request.user).order_by('date')[:3]
    form = PublicationForm()
    if request.method == "POST":
        form = PublicationForm(request.POST,request.FILES or None)
        if form.is_valid():
            text = form.cleaned_data['text']
            fayl = form.cleaned_data['fayl']
            Publication.objects.create(user=request.user,text=text,fayl=fayl)
    form = PublicationForm()
    context={'form':form,'publications':last_publications}
    return render(request,'barrister/advocat_user.html',context)






