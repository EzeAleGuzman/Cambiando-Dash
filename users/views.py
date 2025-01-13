from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, EmailAuthenticationForm
 


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:confirmacionregistro")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def confirmacionregistro(request):
    return render(request, "confirmacionregistro.html")

def login(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home")
            else:
                print("Invalid login")
        else:
            print("Invalid form")
    else:
        form = EmailAuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout(request):
    auth_logout(request)
    return redirect("users:login")

    