
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django import forms
from .choises import SOURCE_CHOICES,BASVURU_CHOICES,DAVALI_CHOICES
import os



class User(AbstractUser):  # auth.models in prebuild user modeli
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# filefield 1.03


class Lawyer(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)  # auth için
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class File(models.Model):

   
    dosya_no = models.CharField(max_length=12,default="",blank=True)
    basvuran = models.CharField(max_length=30)

    # basvurulan = models.CharField(max_length=30)
    davali = models.CharField(
    default='', choices=DAVALI_CHOICES, max_length=100)
    plaka = models.CharField(max_length=10)
    dava_tarihi = models.DateField(max_length=30, null=True, blank=True)
    dosya_durumu = models.CharField(
    default='', choices=SOURCE_CHOICES, max_length=100)
    basvuru_konusu = models.CharField(
    default='', choices=BASVURU_CHOICES, max_length=100)
    kaza_tarihi=models.DateField(max_length=30)
    dosya_notu=models.TextField(max_length=1000,blank=True)
    # avukat silinince dosya da silinecek
    lawyer = models.ForeignKey(Lawyer,null=True, blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.basvuran} {self.davali}"

    @property
    def get_image(self):
        image = self.image_set.all()
        return image

# ------ Signals -----


def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)


class Image(models.Model):
    file_name = models.ForeignKey(File, on_delete=models.CASCADE)
    image = models.FileField(upload_to='class',max_length=260)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image)

    def filename(self):
        return os.path.basename(self.image.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
