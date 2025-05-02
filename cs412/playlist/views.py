from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from .models import Song, Artist, Album, Playlist, PlaylistEntry
from django.db.models.functions import ExtractYear
from .forms import AlbumForm, SongForm, ArtistForm, CustomUserCreationForm, AlbumCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


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
        context['albums'] = artist.album_set.all()
        context['solo_songs'] = artist.song_set.filter(albums=None)
        context['album_count'] = artist.album_set.count()
        context['solo_song_count'] = artist.song_set.filter(albums=None).count()
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

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(id=pk)
        except Playlist.DoesNotExist:
            messages.error(request, "Playlist does not exist.")
            return redirect('playlist:playlist_list')

        # Handle access control
        if not request.user.is_authenticated:
            if playlist.visibility != 'public':
                messages.warning(request, "You must be logged in to view this playlist.")
                return redirect('register')  # Or 'login'
        else:
            if playlist.visibility == 'private' and playlist.owner != request.user:
                messages.error(request, "No access to this private playlist.")
                return redirect('playlist:playlist_list')
            if playlist.visibility == 'shared' and request.user not in playlist.shared_with.all() and playlist.owner != request.user:
                messages.error(request, "No access to this shared playlist.")
                return redirect('playlist:playlist_list')

        entries = PlaylistEntry.objects.filter(playlist=playlist)

        # Get only playlists owned by current user, excluding the current playlist
        user_playlists = Playlist.objects.filter(owner=request.user).exclude(id=playlist.id)

        context = {
            'playlist': playlist,
            'entries': entries,
            'all_playlists': user_playlists,
        }
        return render(request, 'playlist/playlist_detail.html', context)

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name', 'playlist_image', 'visibility', 'shared_with']
    template_name = 'playlist/playlist_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set owner
        playlist = form.save()
        playlist.shared_with.add(self.request.user)  # Give creator access if visibility is shared
        return redirect('playlist:playlist_detail', pk=playlist.pk)

    
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('playlist:music_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'playlist/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('playlist:music_home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('playlist:music_home')  # Redirect to music home page
        else:
            return render(request, 'playlist/login.html', {'error': 'Invalid credentials'})
    return render(request, 'playlist/login.html')

def access_playlist(request, pk):
    try:
        playlist = Playlist.objects.get(id=pk)
    except Playlist.DoesNotExist:
        messages.error(request, "The playlist you're trying to access does not exist.")
        return redirect('playlist:playlist_list')

    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view playlists.")
        return redirect('playlist:playlist_list')

    if playlist.visibility == 'private' and playlist.owner != request.user:
        messages.error(request, "You don’t have access to this private playlist.")
        return redirect('playlist:playlist_list')

    if playlist.visibility == 'shared' and request.user not in playlist.shared_with.all() and playlist.owner != request.user:
        messages.error(request, "You don’t have access to this shared playlist.")
        return redirect('playlist:playlist_list')

    return redirect('playlist:playlist_detail', pk=pk)


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    def post(self, request, pk):
        try:
            playlist = Playlist.objects.get(id=pk)
        except Playlist.DoesNotExist:
            messages.error(request, "Playlist does not exist.")
            return redirect('playlist:playlist_list')

        if playlist.owner != request.user:
            messages.error(request, "You do not have permission to delete this playlist.")
            return redirect('playlist:playlist_list')

        playlist.delete()
        messages.success(request, "Playlist deleted successfully.")
        return redirect('playlist:playlist_list')
    
class EditPlaylistEntryNoteView(LoginRequiredMixin, UpdateView):
    model = PlaylistEntry
    fields = ['user_note']
    template_name = 'playlist/edit_note.html'

    def get_success_url(self):
        return reverse('playlist:playlist_detail', args=[self.object.playlist.id])

    def get_queryset(self):
        # User must own the playlist
        return PlaylistEntry.objects.filter(playlist__user=self.request.user)

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

def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('playlist:artist_list')
    else:
        form = ArtistForm()
    return render(request, 'playlist/add_artist.html', {'form': form})

def add_song_page(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    songs = Song.objects.exclude(playlistentry__playlist=playlist)

    if request.method == 'POST':
        selected_ids = request.POST.getlist('song_ids')
        user_note = request.POST.get('user_note', '')

        for song_id in selected_ids:
            song = Song.objects.get(id=song_id)
            PlaylistEntry.objects.create(
                playlist=playlist,
                song=song,
                added_on=timezone.now(),
                user_note=user_note,
            )
        return redirect('playlist:playlist_detail', pk=playlist.id)

    return render(request, 'playlist/add_song_page.html', {'playlist': playlist, 'songs': songs})


def add_song_to_artist(request, artist_id):
    artist = Artist.objects.get(pk=artist_id)
    
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = artist  # assign the artist to the song
            song.save()
            return redirect('playlist:artist_detail', pk=artist_id)
    else:
        form = SongForm()
    
    return render(request, 'playlist/add_song_to_artist.html', {
        'form': form,
        'artist': artist
    })

def add_album_page(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    albums = Album.objects.all()

    if request.method == 'POST':
        selected_album_ids = request.POST.getlist('album_ids')
        user_note = request.POST.get('user_note', '')

        for album_id in selected_album_ids:
            album = Album.objects.get(id=album_id)
            for song in album.songs.all():
                PlaylistEntry.objects.create(
                    playlist=playlist,
                    song=song,
                    album=album,
                    added_on=timezone.now(),
                    user_note=user_note,
                )
        return redirect('playlist:playlist_detail', pk=playlist.id)

    return render(request, 'playlist/add_album_page.html', {'playlist': playlist, 'albums': albums})



def add_album_to_artist(request, artist_id):
    artist = Artist.objects.get(pk=artist_id)

    if request.method == 'POST':
        form = AlbumCreationForm(request.POST, request.FILES, artist=artist)
        if form.is_valid():
            form.save()
            return redirect('playlist:artist_detail', pk=artist_id)
    else:
        form = AlbumCreationForm()

    return render(request, 'playlist/add_album_to_artist.html', {
        'form': form,
        'artist': artist
    })

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