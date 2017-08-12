from django.contrib.auth.models import User
from django import forms
from .models import Album,Song
from django.contrib.auth import authenticate

class CreateAlbums(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class CreateSong(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class LogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist ")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
        return super(LogInForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    #Confirm_Password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

   # def clean_password(self):
   #     password = self.cleaned_data.get("password")
   #     Confirm_Password = self.cleaned_data.get("Confirm_Password")
   #     if password != Confirm_Password:
   #         forms.ValidationError("Password Must match")
