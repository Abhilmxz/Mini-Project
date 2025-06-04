from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registration', null=True, blank=True)  # Allows null for existing rows
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    state = models.CharField(max_length=100, default='Unknown')  
    address = models.TextField(default='No Address Provided')
    id_proof_type = models.CharField(max_length=50, default='N/A')
    id_proof_number = models.CharField(max_length=50, default='Not Provided')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name
    
    

#PROFILE EDIT AND DETAILS ADDING

class CivicUser(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    dob = models.DateField()
    password = models.CharField(max_length=128)
    state = models.CharField(max_length=50)
    address = models.TextField()
    id_proof = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name




#COMPLAINT FORM

from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    COMPLAINT_CHOICES = [
        ('Noise', 'Noise'),
        ('Pollution', 'Pollution'),
        ('Road damage', 'Road damage'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_CHOICES)
    location = models.CharField(max_length=255)
    proof = models.FileField(upload_to='complaints/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # 👈 New

    def __str__(self):
        return f"{self.user.username} - {self.complaint_type}"

    
    
# feedback

from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


