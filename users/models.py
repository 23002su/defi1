from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    CATEGORY_CHOICES = [
        ('admin', 'Admin'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
    ]
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='etudiant')
    is_password_temp = models.BooleanField(default=True)
    def __str__(self):
        return self.username