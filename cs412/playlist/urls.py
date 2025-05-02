"""
URL routing for the playlist application.
"""

from django.urls import path
from . import views # Import views from the playlist app
from django.contrib.auth import views as auth_views

app_name = "playlist"


urlpatterns = [
    # Homepage or landing page for all music (could be artist view)
    path('', views.MusicHomeView.as_view(), name='music_home'),
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='playlist/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Artist views
    path('artists/', views.ArtistListView.as_view(), name='artist_list'),
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('artist/<int:artist_id>/add-album/', views.add_album_to_artist, name='add_album_to_artist'),
    path('artist/<int:artist_id>/add-song/', views.add_song_to_artist, name='add_song_to_artist'),
    path('artist/add/', views.add_artist, name='add_artist'),

    # Album views
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),

    # Song views
    path('songs/', views.SongListView.as_view(), name='songs'),
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),

    # Playlist views
    path('playlists/', views.PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/new/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlist/<int:pk>/delete/', views.PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlist/<int:pk>/access/', views.access_playlist, name='access_playlist'),


    # Custom: add song to playlist
    path('playlists/<int:playlist_id>/add_song/<int:song_id>/', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('playlists/<int:playlist_id>/add_album/<int:album_id>/', views.add_album_to_playlist, name='add_album_to_playlist'),
    path('playlist/<int:playlist_id>/add_song/', views.add_song_page, name='add_song_page'),
    path('playlist/<int:playlist_id>/add_album/', views.add_album_page, name='add_album_page'),
    path('entry/<int:pk>/edit_note/', views.EditPlaylistEntryNoteView.as_view(), name='edit_entry_note'),
    path('playlist/<int:playlist_id>/manage/', views.manage_playlist_entries, name='manage_playlist_entries'),
]
