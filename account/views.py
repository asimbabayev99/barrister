from django.shortcuts import render
from account.models import CustomUser
from account.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password

# Create your views here.



def login_view(request):
    errors = {}  # may contain authentication errors

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)

            next = request.POST.get('next')
            if next:
                return redirect(next)
            else: 
                return redirect(reverse('home'))
        else:
            errors['message'] = 'Email or password is invalid'


    context = {
        'errors': errors,
        'login': True,
        'register': False,
    }

    return render(request, 'account/login.html', context=context)



def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']

            # new_user = CustomUser(**form.cleaned_data)
            new_user = CustomUser(
                first_name=first_name, last_name=last_name, email=email, phone_number=phone_number
            )
            new_user.password = make_password(password)
            new_user.save()

            return redirect(reverse('login'))

    context = {
        "form": form,
    }

    return render(request, 'account/register.html',context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))