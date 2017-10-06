from django import shortcuts
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Song
from django.db.models import Q
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegForm, CreateAlbums , LogInForm , CreateSong
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']


def index(request):
        all_albums = Album.objects.all().order_by('album_title')
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            all_albums = all_albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'all_albums': all_albums,
                'songs': song_results,
            })

        context = {
            'all_albums': all_albums,
        }
        return render(request, 'music/index.html', context)


def my_album(request):
    if request.user.is_authenticated():
        all_albums = Album.objects.filter(user=request.user)
        return render(request,'music/my_album.html', {'all_albums': all_albums})
    else:
        return redirect('music:user_login')


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.user.is_authenticated():
        t = True
        return render(request, 'music/detail.html', {'album': album, 't': t})
    else:
        return render(request, 'music/detail.html', {'album': album})


def create_albums(request):
    if request.user.is_authenticated():
        form = CreateAlbums(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            album.save()
            return redirect('music:detail', album_id=album.pk)

        #form = CreateAlbums()
        return render(request, 'music/Album_form.html', {'form': form})
    else:
        return render(request, 'music/log_in.html')


def create_song(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.user.is_authenticated() and album.user == request.user:
        print(True)
        form = CreateSong(request.POST or None, request.FILES or None)
        if form.is_valid():
            albums_songs = album.song_set.all()
            for s in albums_songs:
                if s.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/create_song.html', context)
            song = form.save(commit=False)
            song.album = album
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/create_song.html', context)
            song.save()
            return render(request, 'music/detail.html', {'album': album})

        return render(request, 'music/create_song.html', {'form': form,'album': album })
    else:
        return render(request, 'music/log_in.html')


def edit_albums(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    form = CreateAlbums(request.POST or None, request.FILES or None, instance=album)
    if form.is_valid():
        album = form.save(commit=False)
        album.user = request.user
        album.save()
        return redirect('music:detail', album_id=album.pk)

    # form = CreateAlbums(instance=album)
    return render(request, 'music/Album_form.html', {'form': form})


def delete_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    album.delete()
    all_albums = Album.objects.filter(user=request.user)
    return render(request, 'music/my_album.html', {'all_albums': all_albums})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.user.is_authenticated() and album.user == request.user:
        t = True
        song = Song.objects.get(pk=song_id)
        song.delete()
        return render(request, 'music/detail.html', {'album': album, 't': t})
    else:
        return render(request, 'music/log_in.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/my_album.html', {'all_albums': albums})
            else:
                return render(request, 'music/log_in.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/log_in.html',
                          {'error_message': 'Invalid login : Your username or password is incorrect '})
    return render(request, 'music/log_in.html')


def user_logout(request):
    logout(request)
    return render(request, 'music/log_in.html')


def register(request):
    form = UserRegForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    return render(request, 'music/register.html', {'form': form})


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/log_in.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/song.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def filter_song(request):
    all_song = Song.objects.all()
    if request.method == 'POST':
        filter_by = request.POST.get('filter')
        genere = request.POST.get('genere')
        album = Album.objects.filter(genre=genere)
        try:
            song_ids = []
            if filter_by:
                if genere:
                    for a in album:
                        for song in a.song_set.all():
                            song_ids.append(song.pk)
                    song_list = Song.objects.filter(pk__in=song_ids).order_by(filter_by)
                else:
                    for song in all_song.order_by(filter_by):
                        song_ids.append(song.pk)
                    song_list = Song.objects.filter(pk__in=song_ids).order_by(filter_by)
            if genere and filter_by is None:
                for a in album:
                    for song in a.song_set.all():
                        song_ids.append(song.pk)
                song_list = Song.objects.filter(pk__in=song_ids)
        except Album.DoesNotExist:
            song_list = []
        return render(request, 'music/song.html', {
            'song_list': song_list,
        })

def like_song(requst,song_id):
    song = get_object_or_404(Song, pk=song_id)


"""def favorite(request,album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError,Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album':album,
            'error_message': "You did not select any vaild song",
        })
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})"""

"""class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    queryset = Album.objects.all().order_by('album_title')
    page_size=2
    #model = Album
    
    def get_queryset(self):
        return Album.objects.all().order_by('-album_title')

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class CreateAlbumView(generic.CreateView):

    model = Album
    fields = ['artist','album_title','genre','album_logo']

class UpdateAlbumView(generic.UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDeleteView(generic.DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')"""



