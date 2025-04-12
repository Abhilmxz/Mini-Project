from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

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
        form = LoginForm (request.POST)
        if form.is_valid():
            email = form.clean_data['email']
            password = form.clean_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            form.add_error(None, 'Invalid email or password')
    else:
        form =LoginForm()
    return render(request,'login.html',{'form':form})


def homelog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'homelog.html')

def profile(request):
    return render(request, 'profile.html')