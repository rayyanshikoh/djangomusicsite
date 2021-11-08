from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import shutil
from os import path
import zipfile

def extractor(filename, url):
    source_path = url
    with zipfile.ZipFile(source_path, 'r') as zip_ref:
        zip_ref.extractall(f"./media/music/{filename}")



def register_page(request):
    if request.user.is_authenticated:
        return redirect('music:homepage')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('music:login')
        context = {'form':form}
        return render(request, 'music/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('music:homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print('authenticating')
            user = authenticate(request=request, username=username, password=password)
            print('authenticated')
            if user is not None:
                print('logging in')
                login(request, user)
                print('logged in')
                return redirect('music:homepage')
            else:
                messages.info(request, 'Username or Password is incorrect')
                # return render(request, 'music/login.html', context)
        context = {}
        return render(request, 'music/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('music:login')

@login_required(login_url='music:login')
def homepage(request):
    context = {}
    return render(request, 'music/home.html', context)

@login_required(login_url='music:login')
def pricing(request):
    context = {}
    return render(request, 'music/pricing.html', context)

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        new_url = f".{str(uploaded_file_url)}"
        extractor(filename=myfile.name, url=new_url)
        # return render(request, 'music/upload.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
        return redirect('music:homepage')
    return render(request, 'music/upload.html')