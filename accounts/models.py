from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('VENDOR', 'Vendor'),
        ('CUSTOMER', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def is_vendor(self):
        return self.role == 'VENDOR'
    
    def is_customer(self):
        return self.role == 'CUSTOMER'
    
    def __str__(self):
        return self.username