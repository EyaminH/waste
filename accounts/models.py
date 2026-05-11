from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('REPORTER', 'Reporter'),
        ('COLLECTOR', 'Collector'),
        ('ADMIN', 'Admin'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='REPORTER')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
