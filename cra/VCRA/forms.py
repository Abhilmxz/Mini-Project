from django import forms
from .models import UserRegistration
from django.contrib.auth.models import User
from .models import Complaint


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
        fields = ['description', 'complaint_type', 'location', 'proof']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter description', 'class': 'w-full px-4 py-2 border rounded-xl'}),
            'complaint_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-xl'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location', 'class': 'w-full px-4 py-2 border rounded-xl'}),
            'proof': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }