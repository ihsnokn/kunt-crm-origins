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
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import JsonResponse
from django.contrib import messages
from .choises import SOURCE_CHOICES,BASVURU_CHOICES,DAVALI_CHOICES
# CRUD create retrieve update delete + list


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

# LANDING PAGE VIEW

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"
    
@login_required(login_url = "login")
def landing_page(request):
    return render(request, "landing.html")


@login_required(login_url = "login")
def FileListView(request):
    files = File.objects.all().order_by("id")
    context = {
        "files": files
    }
    return render(request, "files/file_list.html", context)




# FILE DETAIL VIEW
@login_required(login_url = "login")
def FileDetail(request,id):

    dosya_durumları=SOURCE_CHOICES
    basvuru_konuları=BASVURU_CHOICES
    davalılar=DAVALI_CHOICES
    file = get_object_or_404(File,id = id)
    images = file.image_set.all()
    context = {
        "file": file,
        "images": images,
        "dosya_durumları": dosya_durumları,
        "basvuru_konuları": basvuru_konuları,
        'davalılar':davalılar,
    }
    return render(request, "files/file_detail.html", context)



@login_required(login_url = "login")
def FileCreateView(request):
    update=False
    lawyer=Lawyer.objects.filter(user=request.user).first()
    form=FileModelForm(request.POST or None)
    formimage=ImageForm(request.POST or None)
    dosya_durumları=SOURCE_CHOICES
    basvuru_konuları=BASVURU_CHOICES
    davalılar=DAVALI_CHOICES  
    lawyers=Lawyer.objects.all()   
    if request.method == 'POST':
        files = request.FILES.getlist("image")
        name= form.data.get('dosya_no')
        if not (form.errors):
                result= classification_helper(files,form,lawyer,update)
                if result == False:
                    messages.warning(request,"Belgenin ismi 180 karakterden fazla olamaz!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                messages.success(request,"Dosya başarılı bir şekilde oluşturuldu.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.warning(request,"Bir sorun oluştu!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request,"files/file_create.html",{'form':form,'formimage':formimage,'dosya_durumları':dosya_durumları,'davalılar':davalılar,"basvuru_konuları":basvuru_konuları,"lawyers":lawyers})

def sign_out(request):
	logout(request)
	return redirect("login") 

# FILE UPDATE VIEW
@login_required(login_url = "login")
def FileUpdateView(request,pk):
    update=True
    lawyer=Lawyer.objects.filter(user=request.user).first()
    file = get_object_or_404(File,id = pk)
    form = FileModelForm()
    images = file.image_set.all()
    formimage=ImageForm(request.POST or None)
    dosya_durumları=SOURCE_CHOICES
    basvuru_konuları=BASVURU_CHOICES
    davalılar=DAVALI_CHOICES
    lawyers=Lawyer.objects.all()   
    if request.method == "POST":
        files = request.FILES.getlist("image")
        name= form.data.get('dosya_no')
        form = FileModelForm(request.POST or None,instance = file)
        print(form.errors)
        if not (form.errors):
            result=classification_helper(files,form,lawyer,update)
            if result == False:
                    messages.warning(request,"Belgenin ismi 180 karakterden fazla olamaz!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            messages.success(request,"Dosya başarılı bir şekilde güncellendi.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        messages.warning(request,"Bir sorun oluştu!")
        return redirect("/files",{'file':file,'dosya_durumları':dosya_durumları,"lawyers":lawyers,"images": images,})
   
    return render(request,"files/file_update.html",{'file':file,'dosya_durumları':dosya_durumları,'davalılar':davalılar,"basvuru_konuları":basvuru_konuları,"lawyers":lawyers,"images": images} )



 
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
    lawyer=Lawyer.objects.filter(user=request.user).first()
    file_array = json.loads(request.body)
    for i in file_array["file_array"]:   
        image= Image.objects.filter(id = i)
        file= File.objects.filter(id=image[0].file_name.id)
        file.update(lawyer=lawyer)
        image.delete()
    return JsonResponse('Payment submitted..', safe=False)
