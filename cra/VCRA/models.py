from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

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



class Complaint(models.Model):
    COMPLAINT_CHOICES = [
        ('Noise', 'Noise'),
        ('Pollution', 'Pollution'),
        ('Road damage', 'Road damage'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_CHOICES)
    location = models.CharField(max_length=255)
    proof = models.FileField(upload_to='complaints/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.complaint_type}"