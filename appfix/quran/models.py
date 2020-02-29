from django.contrib.auth.models import Permission, User
from django.db import models


class Qori(models.Model): 

    user = models.ForeignKey(User, default=1)        
    nama_qori = models.CharField(max_length=250)       
    juz = models.CharField(max_length=500)
    jenis = models.CharField(max_length=100)
    gambar = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):         
        return self.juz + '-' + self.nama_qori 


class Murotal(models.Model):

    qori = models.ForeignKey(Qori, on_delete=models.CASCADE)              
    surah = models.CharField(max_length=250) 
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self): 
        return self.surah 

class Ayat(models.Model):
    title = models.CharField(max_length=100)
    songfile = models.FileField()
    duration = models.FloatField()
    isPlaying = False

    def __str__(self):
        return self.title
 