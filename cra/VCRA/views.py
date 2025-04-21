from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import LoginForm
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserRegistration


# Create your views here.

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile_number']
            dob = form.cleaned_data['date_of_birth']
            password = form.cleaned_data['password']

            # Check if the email (username) already exists
            if User.objects.filter(username=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                try:
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = full_name  # Optional: Set the user's full name
                    user.save()

                    # Now create a UserRegistration record for the newly created user
                    user_registration = UserRegistration.objects.create(
                        user=user,
                        full_name=full_name,
                        mobile_number=mobile,
                        date_of_birth=dob,
                        email=email,
                        password=password,
                    )
                    user_registration.save()

                    return redirect('login')  # Redirect after successful registration
                except IntegrityError:
                    form.add_error(None, 'An unexpected error occurred. Please try again.')
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
                    return redirect('homelog')
            form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})



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

def complaint(request):
    return render(request, 'complaint.html')

def adminover(request):
    return render(request, 'adminover.html')