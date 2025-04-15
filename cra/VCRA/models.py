from django.db import models

# Create your models here.

class UserRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    state = models.CharField(max_length=100)
    address = models.TextField()
    id_proof_type = models.CharField(max_length=50)
    id_proof_number = models.CharField(max_length=50)


    def __str__(self):
        return self.full_name

