from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  # ログイン後はダッシュボードへ
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("home")
