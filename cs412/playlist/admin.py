from django.contrib import admin
from .models import Song, Artist, Album, Playlist, PlaylistEntry

# Register your models here.
admin.site.register(Song)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Playlist)
admin.site.register(PlaylistEntry)


