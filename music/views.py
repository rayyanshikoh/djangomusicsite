from re import template
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, Http404
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import shutil
import os
from os import path
import zipfile

from tinytag import TinyTag
from .models import Album, Artist

# Additional functions and objects to assist views

class Music:
    def __init__(self, album, albumartist, year, genre, title, artist):
        self.album = album
        self.albumartist = albumartist
        self.year = year
        self.genre = genre
        self.title = title
        self.artist = artist

class Music1:
    def __init__(self, album, albumartist, year, genre, title, artist, location):
        self.album = album
        self.albumartist = albumartist
        self.year = year
        self.genre = genre
        self.title = title
        self.artist = artist
        self.location = location


def deleter(url):
    source_path = str(url)
    if os.path.exists(source_path):
        os.remove(source_path)
    else:
        print("The file does not exist")


def extractor(filename, url):
    source_path = url
    filename1 = filename.split('.zip')
    filename1 = str(filename1[0])
    filename_webfile = str(source_path).replace('%20', ' ')
    print(filename_webfile)
    with zipfile.ZipFile(filename_webfile, 'r') as zip_ref:
        zip_ref.extractall(f"./media/music/{filename1}")
    deleter(filename_webfile)
    new_url1 = f"{filename1}/{filename1}"
    music_adder(f"./media/music/{new_url1}")


def music_adder(url):
    list = []
    for filename in os.listdir(url):
        if filename.endswith(".mp3") or filename.endswith(".py"): 
            tag = TinyTag.get(f"{url}/{filename}")
            album = tag.album
            title = tag.title
            albumartist = tag.albumartist
            artist = tag.artist
            genre = tag.genre
            year = tag.year
            print(f"{title} {artist} {album} {albumartist} {genre} {year}")
            list.append(Music(album, albumartist, year, genre, title, artist))
    first = list[0]
    print(first.albumartist)
    q = Artist(artist_name = str(albumartist), artist_picture_name = "N/a", artist_description = "N/a")
    q.save()
    q.album_set.create(album_name = album, album_filename_url = f"{url}/{filename}", release_date = year, album_art = "N/A")

# Define your views here


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

@login_required(login_url='music:login')
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        new_url = f".{str(uploaded_file_url)}"
        extractor(filename=myfile.name, url=new_url)
        return redirect('music:homepage')
    return render(request, 'music/upload.html')

@login_required(login_url='music:login')
def artists(request):
    artists_list = Artist.objects.all()
    context = {
        'artists_list':artists_list,
    }
    return render(request, 'music/artists.html', context)


@login_required(login_url='music:login')
def albums(request, artist_id):
    try:
        artist = Artist.objects.get(pk=artist_id)
        print(artist)
    except Artist.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'music/album.html', {'artist': artist})


@login_required(login_url='music:login')
def songs(request, album_id, artist_id):
    print(album_id)
    album = Album.objects.get(pk=album_id)
    album1 = album
    url = album.album_filename_url
    print(url)
    context = []
    cover = str(url)[1:]
    for filename in os.listdir(url):
        if filename.endswith(".mp3") or filename.endswith(".py"): 
            tag = TinyTag.get(f"{url}{filename}")
            location = (f"{url}{filename}")
            location = location[14:]
            album = tag.album
            title = tag.title
            albumartist = tag.albumartist
            artist = tag.artist
            genre = tag.genre
            year = tag.year
            context.append(Music1(album, albumartist, year, genre, title, artist, location))   
    return render(request, 'music/songs.html', {'context':context, 'album':album, 'album1':album1, 'cover':cover})