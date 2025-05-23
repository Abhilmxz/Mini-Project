from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .forms import LoginForm
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserRegistration
from django.contrib import messages
from .forms import ComplaintForm
from django.contrib.auth.decorators import login_required
from .models import Complaint

from django.core.mail import send_mail
from django.conf import settings
from .forms import ForgotPasswordForm
import random
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.

def home(request):
    return render(request, 'home.html')

#USER REGISTRATION FUNCTION

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


#LOGIN FUNCTION

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

# Homelog Function

def homelog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'homelog.html')



# Forgotten Password Functions

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                code = str(random.randint(1000, 9999))
                request.session['reset_email'] = email
                request.session['reset_code'] = code

                send_mail(
                    'Your Password Reset Code',
                    f'Here is your 4-digit code: {code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                return redirect('verify_code')
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})



def verify_code(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        if code_entered == request.session.get('reset_code'):
            return redirect('set_new_password')
        else:
            messages.error(request, 'Invalid code. Please try again.')

    return render(request, 'verify_code.html')



def set_new_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            email = request.session.get('reset_email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been changed.')
            return redirect('login')
    return render(request, 'set_new_password.html')




#COMPLAINT FUNCTION

@login_required
def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # Assign the logged-in user
            complaint.save()
            messages.success(request, "Complaint submitted successfully!")
            return redirect('complaints_list')  # Redirect to a complaints list or another page after submission
        else:
            messages.error(request, "There was an error with your submission. Please try again.")
    else:
        form = ComplaintForm()

    # Render the form if GET request or on error
    return render(request, 'complaint.html', {'form': form})


@login_required
def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # Assign the logged-in user
            complaint.save()
            messages.success(request, "Complaint submitted successfully!")
            return redirect('my_complaints')  # Redirect to the complaints list
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = ComplaintForm()

    return render(request, 'complaint.html', {'form': form})


@login_required
def my_complaints(request):
    # Fetch the logged-in user's complaints
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'my_complaints.html', {'complaints': complaints})

def view_proof(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'view_proof.html', {'complaint': complaint})


@login_required
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id, user=request.user)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, "Complaint updated successfully.")
            return redirect('my_complaints')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'edit_complaint.html', {'form': form})

@login_required
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id, user=request.user)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, "Complaint deleted successfully.")
        return redirect('my_complaints')
    return render(request, 'delete_confirm.html', {'complaint': complaint})





def profile(request):
    return render(request, 'profile.html')



def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')




#Admin Functions

def adminover(request):
    return render(request, 'adminover.html')


def user_manage(request):
    return render(request, 'user_manage.html')

def admin_comp(request):
    return render(request, 'admin_comp.html')


def feedback(request):
    return render(request, 'feedback.html')