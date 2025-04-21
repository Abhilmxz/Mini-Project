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
