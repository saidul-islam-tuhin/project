from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.index , name='index'),
    # /music/my_album/
    url(r'^my_album/$', views.my_album, name='my_album'),
    # music/21/
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    # music/21/create_song
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    # music/create_album
    url(r'^create_album/$', views.create_albums, name='create_albums'),
    # music/23/edit_album
    url(r'^(?P<album_id>[0-9]+)/edit_album/$', views.edit_albums, name='edit_albums'),
    # music/23/delete_album
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    # music/23/delete_song
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    # music/login/
    url(r'^login/$', views.user_login, name='user_login'),
    # music/logout/
    url(r'^logout/$', views.user_logout, name='user_logout'),
    # music/register
    url(r'^register/$', views.register, name='register'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^filter/song$', views.filter_song, name='filter_song'),
    # music/23/like
    url(r'^(?P<song_id>[0-9]+)/like/$', views.like_song, name='like_song'),









    # url(r'^$', views.IndexView.as_view() , name='index' ),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #music/add
    #url(r'^add/$', views.CreateAlbumView.as_view() , name='create_album' ),
    #music/delete
    #url(r'^delete/$', views.AlbumDeleteView.as_view(), name='delete_album'),


    #/music/21/favorite/
     #url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

]