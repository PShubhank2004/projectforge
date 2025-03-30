from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register,logout_user


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
]
