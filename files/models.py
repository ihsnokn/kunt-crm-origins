
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django import forms
from .choises import SOURCE_CHOICES,BASVURU_CHOICES,DAVALI_CHOICES
import os
from django_quill.fields import QuillField


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



class File_Notes(models.Model):
    file = models.OneToOneField(File, on_delete=models.CASCADE)
    note = QuillField(blank=True)
    def __str__(self):
        return self.file

class Image(models.Model):
    file_name = models.ForeignKey(File, on_delete=models.CASCADE)
    image = models.FileField(upload_to='class',max_length=280)
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


class Masraflar(models.Model):
    file_name = models.ForeignKey(File, on_delete=models.CASCADE)
    eksper_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    dava_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    bk_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    islah_harci = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    karsi_vekalet_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    karsi_vekalet_date=models.DateField(max_length=30,null=True, blank=True)


    #Gelen ödemeler
    davalidan_gelen_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    davalidan_gelen_date=models.DateField(max_length=30,null=True, blank=True)

    icradan_gelen_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    icradan_gelen_date=models.DateField(max_length=30,null=True, blank=True)

    muvekkile_gonderilen_fee = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    muvekkile_gonderilen_date=models.DateField(max_length=30,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return str(self.file_name)



def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        Masraflar.objects.create(file_name=instance)
        File_Notes.objects.create(file=instance)


post_save.connect(post_user_created_signal, sender=File)
