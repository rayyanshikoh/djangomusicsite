from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .forms import CreateUserForm

def homepage(request):
    return render(request, 'music/home.html', {})

def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        
    context = {'form':form}
    return render(request, 'music/register.html', context)

def login_page(request):
    context = {}
    return render(request, 'music/login.html', context)

def pricing(request):
    context = {}
    return render(request, 'music/pricing.html', context)