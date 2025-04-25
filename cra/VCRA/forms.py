from django import forms
from .models import UserRegistration
from django.contrib.auth.models import User
from .models import Complaint
from django.core.exceptions import ValidationError


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


def clean_mobile_number(self):
    mobile_number = self.cleaned_data.get('mobile_number')
    return mobile_number

def clean_email(self):
    email = self.cleaned_data.get('email')
    return email

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)



class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ['user', 'created_at']
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'Enter description',
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

    # Validation for proof (file upload)
    def clean_proof(self):
        proof = self.cleaned_data.get('proof', None)
        if proof:
            # File size check (example: max 5MB)
            if proof.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be less than 5 MB.")

            # File type check (example: allow only images or videos)
            if not proof.name.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi')):
                raise ValidationError("File type must be JPG, PNG, MP4, MOV, or AVI.")
        
        return proof
