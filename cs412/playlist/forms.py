from django import forms
from django.contrib.auth.models import User
from .models import Artist, Song, Album, Playlist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'hometown', 'height', 'debut_year', 'profile_image']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'song_image'] 

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'release_date', 'album_image', 'genre', 'songs']
        widgets = {
            'songs': forms.CheckboxSelectMultiple()
        }

class AlbumCreationForm(forms.ModelForm):
    new_songs = forms.CharField(
        required=False,
        help_text="Enter song titles separated by commas.",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Track 1, Track 2, Track 3'})
    )

    class Meta:
        model = Album
        fields = ['title', 'release_date', 'album_image', 'genre']

    def __init__(self, *args, **kwargs):
        self.artist = kwargs.pop('artist', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        album = super().save(commit=False)
        album.artist = self.artist
        if commit:
            album.save()

        song_titles_raw = self.cleaned_data.get('new_songs', '')
        song_titles = [title.strip() for title in song_titles_raw.split(',') if title.strip()]
        for title in song_titles:
            song, created = Song.objects.get_or_create(title=title)
            album.songs.add(song)

        return album

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'playlist_image', 'visibility', 'shared_with']
        widgets = {
            'shared_with': forms.CheckboxSelectMultiple
        }