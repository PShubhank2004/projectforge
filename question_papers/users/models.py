from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def save(self, *args, **kwargs):
        if self.email.endswith("@gitam.edu"):
            self.role = "teacher"
        elif self.email.endswith("@gitam.in"):
            self.role = "student"
        super().save(*args, **kwargs)
