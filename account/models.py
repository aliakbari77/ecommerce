from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.username}'
    
    def __repr__(self):
        return f'{self.username}'
