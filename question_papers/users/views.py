'''from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('repository:paper_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    return render(request, 'users/login.html')


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_user(request):
    logout(request)
    return redirect('login') ''' # Redirect to the home/papers page




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm  # ✅ Use the correct form

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # ✅ Correct form
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ Log in the new user
            return redirect('repository:paper_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('repository:paper_list')
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
