from distutils.log import Log
import os
from django.shortcuts import render, redirect, reverse,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, request
from files.helper import classification_helper
from .models import File, Image, Lawyer
from .forms import FileForm, FileModelForm, CustomUserCreationForm, ImageForm
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib import messages
# CRUD create retrieve update delete + list
SOURCE_CHOICES = (
        # database name and display value respectively
        ('evrak_bekleyen', 'Evrak Bekleyen'),
        ('talep', 'Talep'),
        ('dava_acilacak', 'Dava Açılacak'),
        ('ara_karar', 'Ara Karar'),
        ('bilir_kisi_raporu', 'Bilir Kişi Raporu'),
        ('karar', 'Karar'),
        ('icra', 'İcra'),
        ('odeme_bekleyen', 'Ödeme Bekleyen'),
        ('kapanis', 'Kapanış'),
        ('ikinci_talep', '2. Talep'),
    )


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

# LANDING PAGE VIEW
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

def landing_page(request):
    return render(request, "landing.html")

# FILE LIST VIEW
# class FileListView(LoginRequiredMixin, generic.ListView):
#     template_name = "files/file_list.html"
#     queryset = File.objects.all().order_by("-id")
#     context_object_name = "files"

# def file_list(request):

#     files = File.objects.all().order_by("-id")
#     print(files)
#     context = {
#         "files": files
#     }

#     return render(request, "files/file_list.html", context)



def FileListView(request):
    files = File.objects.all().order_by("id")

    context = {
        "files": files
    }
    return render(request, "files/file_list.html", context)




# FILE DETAIL VIEW

def FileDetail(request,id):
    file = get_object_or_404(File,id = id)
    images = file.image_set.all()
    context = {
        "file": file,
        "images": images,
    }
    return render(request, "files/file_detail.html", context)

def FileCreateView(request):
    

    form=FileModelForm(request.POST or None)
    formimage=ImageForm(request.POST or None)
    dosya_durumları=SOURCE_CHOICES
    lawyers=Lawyer.objects.all()   
    if request.method == 'POST':
        files = request.FILES.getlist("image")
        name= form.data.get('dosya_no')
        if not (form.errors):
                classification_helper(name,files,form)
                messages.success(request,"Dosya başarılı bir şekilde oluşturuldu.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.warning(request,"Bir sorun oluştu!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request,"files/file_create.html",{'form':form,'formimage':formimage,'dosya_durumları':dosya_durumları,"lawyers":lawyers})

def sign_out(request):
	logout(request)
	return redirect("login") 

# FILE UPDATE VIEW

def FileUpdateView(request,pk):

    file = get_object_or_404(File,id = pk)
    form = FileModelForm()
    images = file.image_set.all()
    formimage=ImageForm(request.POST or None)
    dosya_durumları=SOURCE_CHOICES
    lawyers=Lawyer.objects.all()   
    if request.method == "POST":
        files = request.FILES.getlist("image")
        name= form.data.get('dosya_no')
        form = FileModelForm(request.POST or None,instance = file)
        print(form.errors)
        if not (form.errors):
            classification_helper(name,files,form)
            messages.success(request,"Dosya başarılı bir şekilde güncellendi.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # file = form.save(commit=False)
            # file.save()
            # file_name = File.objects.filter(dosya_no=file.dosya_no).first()
        messages.warning(request,"Bir sorun oluştu!")
        return redirect("/files",{'file':file,'dosya_durumları':dosya_durumları,"lawyers":lawyers,"images": images,})
   
    return render(request,"files/file_update.html",{'file':file,'dosya_durumları':dosya_durumları,"lawyers":lawyers,"images": images} )



 
# FILE DELETE VIEW

class FileDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "files/file_delete.html"
    queryset = File.objects.all()

    def get_success_url(self):
        return reverse("files:file-list")

def file_delete(request, pk):
    file = File.objects.get(id=pk)
    file.delete()
    return redirect("/files")


def FileDeleteUpdate(request):
    file_array = json.loads(request.body)
    print(file_array)
    for i in file_array["file_array"]:
       # print(i)
        image= Image.objects.filter(id = i)
        image.delete()
    return JsonResponse('Payment submitted..', safe=False)