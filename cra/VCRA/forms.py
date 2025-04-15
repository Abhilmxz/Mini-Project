from django import forms
from .models import UserRegistration

from django import forms
from .models import UserRegistration

from django import forms
from .models import UserRegistration

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['full_name', 'mobile_number', 'date_of_birth', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(), 
        }


def clean_mobile_number(self):
    mobile_number = self.cleaned_data.get('mobile_number')
    return mobile_number

def clean_email(self):
    email = self.cleaned_data.get('email')
    return email

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label='Password',max_length=255)