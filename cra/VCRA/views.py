from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect if valid
        else:
            print(form.errors)  # Optional: See errors in console
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password']
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
            form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
        
    return render(request, 'login1.html', {'form': form})



def homelog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'homelog.html')

def profile(request):
    return render(request, 'profile.html')



def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')