from django import forms
from django.contrib.auth.models import User
 
from .models import Qori, Murotal

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class MurotalForm(forms.ModelForm):

    class Meta:
        model = Murotal
        fields = ['surah','audio_file'] 

class QoriForm(forms.ModelForm):

    class Meta:
        model = Qori
        fields =['nama_qori','juz','jenis', 'gambar']