from django import forms
from .models import UserRegistration, Complaint
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Feedback
from .models import UserProfile
from .models import ContactMessage

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['full_name', 'mobile_number', 'date_of_birth', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class LoginForm(forms.Form):
    email_or_username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={'placeholder': 'Email or Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'mobile_number', 'dob', 'state', 'address', 'id_proof', 'id_number']
    

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ['user', 'created_at', 'status']
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter description',
                'rows': 5,
                'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'complaint_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter location',
                'class': 'w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'proof': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'id': 'file-upload'
            }),
        }

    def clean_proof(self):
        proof = self.cleaned_data.get('proof', None)
        if proof:
            if proof.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be less than 5 MB.")
            if not proof.name.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi')):
                raise ValidationError("Invalid file type. Only images or videos are allowed.")
        return proof


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']  # use message, not feedback


#contact message save

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']