from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, EmailAuthenticationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Usar auth_login para iniciar sesión automáticamente
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
                if user.is_active:
                    auth_login(request, user)  # Usar auth_login para evitar conflicto
                    return redirect("gestioncamas:dashboard")
                else:
                    return render(request, "account_inactive.html")
            else:
                return render(request, "login.html", {"form": form, "error": "Invalid login"})
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid form"})
    else:
        form = EmailAuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout(request):
    auth_logout(request)
    return redirect("users:login")

def recover_password(request):
    return render(request, "recover_password.html")
    