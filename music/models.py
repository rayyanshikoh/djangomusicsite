from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Artist(models.Model):
    artist_name = models.CharField(max_length=100)
    artist_picture_name = models.CharField(max_length=100)
    artist_description = models.CharField(max_length=100)
    def __str__(self):
        return self.artist_name

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=100)
    album_filename_url = models.CharField(max_length=100)
    release_date = models.IntegerField()
    album_art = models.CharField(max_length=100)
    def __str__(self):
        return self.album_name

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100)
    song_artists = models.CharField(max_length=100)