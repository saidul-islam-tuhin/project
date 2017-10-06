from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User


# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.ImageField(width_field="width_field",height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist

    def get_absolute_url(self):
        return reverse('music:index')


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    audio_file = models.FileField(default='')
    song_title = models.CharField(max_length=250)
    upload_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

    #def get_absolute_url(self):
        #return reverse('music:detail', kwargs={'album_id': self.pk})