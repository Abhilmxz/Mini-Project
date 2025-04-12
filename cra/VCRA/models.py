from django.db import models

# Create your models here.

class UserRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

