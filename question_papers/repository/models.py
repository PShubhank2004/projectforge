from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings




class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class QuestionPaper(models.Model):
    SUBJECT_CHOICES = [
        ('cse', 'Computer Science'),
        ('ece', 'Electronics & Communication'),
        ('eee', 'Electrical & Electronics'),
        ('mech', 'Mechanical'),
        ('civil', 'Civil Engineering'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)  # Paper title (optional)
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES)
    course = models.CharField(max_length=100)  # Ex: B.Tech CSE
    year = models.IntegerField()  # Year of the paper
    file = models.FileField(upload_to='papers/')  # PDF File Upload
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    tags = models.ManyToManyField(Tag, blank=True)  # Tags for repeated questions


    def __str__(self):
        return f"{self.subject} - {self.course} ({self.year})"


    



