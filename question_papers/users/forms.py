from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith("@gitam.in") and not email.endswith("@gitam.edu"):
            raise forms.ValidationError("Only Gitam email addresses are allowed!")
        return email
