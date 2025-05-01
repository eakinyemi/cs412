from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from .models import Song, Artist, Album, Playlist, PlaylistEntry
from django.db.models.functions import ExtractYear

# Homepage
class MusicHomeView(TemplateView):
    template_name = 'playlist/music_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = Song.objects.all()
        context['artists'] = Artist.objects.all()
        context['albums'] = Album.objects.all()
        return context

# Song Views
class SongListView(ListView):
    model = Song
    template_name = 'playlist/song_list.html'
    context_object_name = 'songs'

    def get_queryset(self):
        qs = Song.objects.all()
        filter_val = self.request.GET.get('filter')

        if filter_val == 'alphabetical':
            qs = qs.order_by('title')
        elif filter_val == 'artist':
            qs = sorted(qs, key=lambda s: s.albums.first().artist.name if s.albums.exists() else "")
        elif filter_val and filter_val.startswith('year_'):
            year = filter_val.split('_')[1]
            qs = qs.filter(albums__release_date__year=year)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_years = Album.objects.annotate(year=ExtractYear('release_date')).values_list('year', flat=True).distinct()
        context['years'] = sorted(set(all_years))
        return context

class SongDetailView(DetailView):
    model = Song
    template_name = 'playlist/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = self.object

        # Determine image to show
        image_url = None
        if song.song_image:
            image_url = song.song_image.url
        else:
            for album in song.albums.all():
                if album.album_image:
                    image_url = album.album_image.url
                    break

        context['display_image_url'] = image_url
        return context

# Artist Views
class ArtistListView(ListView):
    model = Artist
    template_name = 'playlist/artist_list.html'
    context_object_name = 'artists'

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'playlist/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.object
        context['albums'] = Album.objects.filter(artist=artist)
        return context

# Album Views
class AlbumListView(ListView):
    model = Album
    template_name = 'playlist/album_list.html'
    context_object_name = 'albums'

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'playlist/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.songs.all()
        return context

# Playlist Views
class PlaylistListView(ListView):
    model = Playlist
    template_name = 'playlist/playlist_list.html'
    context_object_name = 'playlists'

class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'playlist/playlist_detail.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.object
        entries = PlaylistEntry.objects.filter(playlist=playlist)

        # Add raw entries to context for looping in template
        context['entries'] = entries

        # Build song + image URL tuples
        songs_with_images = []
        for entry in entries:
            if entry.song:
                song_image = entry.song.song_image.url if entry.song.song_image else (
                    entry.song.albums.first().album_image.url if entry.song.albums.first() and entry.song.albums.first().album_image else None
                )
                songs_with_images.append((entry.song, song_image))

        context['songs_with_images'] = songs_with_images
        return context

class PlaylistCreateView(CreateView):
    model = Playlist
    fields = ['name', 'user_email', 'playlist_image']
    template_name = 'playlist/playlist_form.html'

    def get_success_url(self):
        return reverse('playlist_detail', kwargs={'pk': self.object.pk})

# Add Song to Playlist
def add_song_to_playlist(request, playlist_id, song_id):
    try:
        playlist = Playlist.objects.get(pk=playlist_id)
        song = Song.objects.get(pk=song_id)
        PlaylistEntry.objects.create(
            playlist=playlist,
            song=song,
            added_on=timezone.now()
        )
    except (Playlist.DoesNotExist, Song.DoesNotExist):
        return redirect('playlist_list')  # fallback if something went wrong

    return redirect(reverse('playlist_detail', kwargs={'pk': playlist_id}))

# Add Album to Playlist (adds each song from album)
def add_album_to_playlist(request, playlist_id, album_id):
    playlist = Playlist.objects.get(id=playlist_id)
    album = Album.objects.get(id=album_id)
    for song in album.songs.all():
        PlaylistEntry.objects.create(
            playlist=playlist,
            song=song,
            added_on=timezone.now()
        )
    return redirect(reverse('playlist:playlist_detail', kwargs={'pk': playlist_id}))

# Add a song to playlist
def add_song_page(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    songs = Song.objects.all()

    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        if song_id:
            song = Song.objects.get(id=song_id)
            PlaylistEntry.objects.create(
                playlist=playlist,
                song=song,
                added_on=timezone.now()
            )
            return redirect(reverse('playlist:playlist_detail', kwargs={'pk': playlist_id}))

    return render(request, 'playlist/add_song_page.html', {'playlist': playlist, 'songs': songs})


# Add album to playlist — adds all its songs individually
def add_album_page(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    albums = Album.objects.all()

    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        if album_id:
            album = Album.objects.get(id=album_id)
            for song in album.songs.all():
                PlaylistEntry.objects.create(
                    playlist=playlist,
                    song=song,
                    album=album,
                    added_on=timezone.now()
                )
            return redirect(reverse('playlist:playlist_detail', kwargs={'pk': playlist_id}))

    return render(request, 'playlist/add_album_page.html', {'playlist': playlist, 'albums': albums})

def manage_playlist_entries(request, playlist_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        entry_ids = request.POST.getlist('selected_entries')
        entries = PlaylistEntry.objects.filter(id__in=entry_ids)

        if action == 'delete':
            entries.delete()

        elif action == 'move':
            new_playlist_id = request.POST.get('move_to_playlist_id')
            if new_playlist_id:
                new_playlist = Playlist.objects.get(id=new_playlist_id)
                for entry in entries:
                    entry.playlist = new_playlist
                    entry.save()

    return redirect('playlist:playlist_detail', pk=playlist_id)