# ================================
#           IMPORTS
# ================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from .models import Feedback
# from .forms import FeedbackForm  # assuming you have a form
from django.http import HttpResponseForbidden
from .forms import CivicUserForm
from .models import CivicUser
from django.http import HttpResponse

import time
import secrets
import random

from .forms import (
    UserRegistrationForm,
    LoginForm,
    ComplaintForm,
    ForgotPasswordForm,
    CustomUserForm
)

from .models import (
    UserRegistration,
    Complaint,
    Feedback
)


# ================================
#           BASIC VIEWS
# ================================

def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def delete_account(request):
    return render(request, 'delete_pro.html')

def logout_view(request):
    return render(request, 'logout.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')


# ================================
#       USER REGISTRATION
# ================================

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile_number']
            dob = form.cleaned_data['date_of_birth']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                try:
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = full_name
                    user.save()

                    user_registration = UserRegistration.objects.create(
                        user=user,
                        full_name=full_name,
                        mobile_number=mobile,
                        date_of_birth=dob,
                        email=email,
                        password=password,
                    )
                    user_registration.save()

                    return redirect('login')
                except IntegrityError:
                    form.add_error(None, 'An unexpected error occurred. Please try again.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


# ================================
#           LOGIN VIEWS
# ================================

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


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('homelog')
        else:
            messages.error(request, 'Invalid email or password.')
    return redirect('login')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/adminover/')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return redirect('login')


def homelog(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'homelog.html')


# ================================
#      FORGOT PASSWORD FLOW
# ================================

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(secrets.randbelow(900000) + 100000)
                request.session['reset_email'] = email
                request.session['reset_code'] = otp
                request.session['otp_time'] = time.time()

                send_mail(
                    'Your Password Reset OTP',
                    f'Your OTP for password reset is: {otp}\nDo not share this code with anyone.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, f'An OTP has been sent to {email}. Please check your email.')
                return redirect('verify_code')
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        session_code = request.session.get('reset_code')
        otp_time = request.session.get('otp_time')

        if code_entered == session_code:
            if otp_time and (time.time() - otp_time) > 300:
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('forgot_password')
            else:
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
            if not email:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('forgot_password')

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    messages.error(request, 'New password cannot be the same as the old password.')
                    return redirect('set_new_password')

                user.set_password(password)
                user.save()

                request.session.pop('reset_email', None)
                request.session.pop('reset_code', None)
                request.session.pop('otp_time', None)

                messages.success(request, 'Your password has been changed successfully. Please login.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found. Please try again.')

    return render(request, 'set_new_password.html')


# ================================
#           PROFILE VIEWS
# ================================


def civic_form_view(request, user_id=None):
    instance = CivicUser.objects.filter(pk=user_id).first() if user_id else None

    if request.method == 'POST':
        form = CivicUserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print("❌ Form is not valid:", form.errors)
    else:
        form = CivicUserForm(instance=instance)

    return render(request, 'your_app/civic_form.html', {'form': form})

def success_view(request):
    return HttpResponse("✅ Form submitted successfully!")

# ================================
#         COMPLAINT VIEWS
# ================================

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
            complaint.user = request.user
            complaint.save()
            messages.success(request, "Complaint submitted successfully!")
            return redirect('my_complaints')
        else:
            print(form.errors.as_json())  # Debugging output
            messages.error(request, "There was an error with your submission. Please check the fields below.")
    else:
        form = ComplaintForm()

    return render(request, 'complaint.html', {'form': form})


@login_required
def my_complaints(request):
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


# ================================
#         FEEDBACK VIEWS
# ================================

def submit_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback', '').strip()
        if feedback:
            # Save feedback to database or process it here
            messages.success(request, "Thank you! Your feedback has been submitted.")
        else:
            messages.error(request, "Please enter some feedback before submitting.")
    return redirect('homelog')  # redirect to homepage or wherever


def feedback_view(request):
    # Your feedback logic here
    return render(request, 'feedback.html')

@login_required
def feedback_admin_view(request):
    # Only allow staff (admin) users to access this view
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    feedback_entries = Feedback.objects.order_by('-created_at')
    return render(request, 'feedback.html', {'feedback_entries': feedback_entries})

# ================================
#         ADMIN FUNCTIONS
# ================================

def adminover(request):
    users = UserRegistration.objects.all().order_by('-created_at')
    return render(request, 'adminover.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def adminover(request):
    users = UserRegistration.objects.all().order_by('-created_at')
    return render(request, 'your_app/adminover.html', {'users': users})

def user_manage(request):
    users = UserRegistration.objects.all()
    return render(request, 'user_manage.html', {'users': users})


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form})


def delete_user(request, user_id):
    user = get_object_or_404(UserRegistration, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('user_manage')


def admin_complaints_view(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin_complaints.html', {'complaints': complaints})


def update_complaint_status(request, pk, status):
    complaint = get_object_or_404(Complaint, pk=pk)
    if status in ['accepted', 'rejected']:
        complaint.status = status
        complaint.save()
    return redirect('admin_comp')


@staff_member_required
def edit_admin_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, "Complaint updated.")
            return redirect('admin_comp')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'admin/edit_complaint.html', {'form': form, 'complaint': complaint})
