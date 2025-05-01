from django.db import models
from django.utils import timezone


class Artist(models.Model):
    name = models.CharField(max_length=100)
    hometown = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    debut_year = models.IntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=100)
    song_image = models.ImageField(upload_to='song_images/', blank=True, null=True)


    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    album_image = models.ImageField(upload_to='album_images/', blank=True, null=True)
    genre = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song, blank=True, related_name='albums')

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

    def song_count(self):
        return self.songs.count()


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    playlist_image = models.ImageField(upload_to='playlist_images/', blank=True, null=True)
    user_email = models.EmailField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_songs(self):
        return self.playlistentry_set.count()


class PlaylistEntry(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    added_on = models.DateTimeField(default=timezone.now)
    user_note = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.song:
            return f"{self.song.title} in {self.playlist.name}"
        elif self.album:
            return f"{self.album.title} (album) in {self.playlist.name}"
        return f"Entry in {self.playlist.name}"
