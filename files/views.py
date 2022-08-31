from distutils.log import Log
import os
from django.shortcuts import render, redirect, reverse,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, request
from files.helper import classification_helper
from .models import File, File_Notes, Image, Lawyer, Masraflar
from .forms import FileForm, FileModelForm, CustomUserCreationForm, FileNoteForm, ImageForm,FeeModelForm
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import JsonResponse
from django.contrib import messages
from .choises import SOURCE_CHOICES,BASVURU_CHOICES,DAVALI_CHOICES
from django.conf import settings
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
def FileDetail(request,pk):

    dosya_durumları=SOURCE_CHOICES
    basvuru_konuları=BASVURU_CHOICES
    davalılar=DAVALI_CHOICES
    file = get_object_or_404(File,id = pk)
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
    file_obj = File.objects.filter(id = pk).first()
    note = File_Notes.objects.filter(file=file_obj).first()
    form = FileModelForm()
    form_note = FileNoteForm()
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
        form_note = FileNoteForm(request.POST or None,instance = note)
        print(form_note.errors)
        if not (form.errors and form_note.errors):
            result=classification_helper(files,form,lawyer,update)
            if result == False:
                    messages.warning(request,"Belgenin ismi 180 karakterden fazla olamaz!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            form_note.save()

            messages.success(request,"Dosya başarılı bir şekilde güncellendi.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        messages.warning(request,"Bir sorun oluştu!")
        return redirect("/files",{'note':note,'form_note':form_note,'file':file,'dosya_durumları':dosya_durumları,"lawyers":lawyers,"images": images,})
   
    return render(request,"files/file_update.html",{'form_note':form_note,'file':file,'note':note,'form':form,'dosya_durumları':dosya_durumları,'davalılar':davalılar,"basvuru_konuları":basvuru_konuları,"lawyers":lawyers,"images": images} )





@login_required(login_url = "login")
def FileUpdateFeeView(request,pk):

    lawyer=Lawyer.objects.filter(user=request.user).first()
    file = get_object_or_404(File,id = pk)
    file_fee = get_object_or_404(Masraflar,file_name = pk)
    form = FeeModelForm()

    lawyers=Lawyer.objects.all() 
    images = file.image_set.all()  
    if request.method == "POST":
        form = FeeModelForm(request.POST or None,instance = file_fee)
        if not (form.errors):
            fee = form.save(commit=False)
            fee.save()
            file.lawyer=lawyer 
            file.save()         
            messages.success(request,"Masraflar başarılı bir şekilde güncellendi.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.warning(request,"Bir sorun oluştu!")
        return redirect("/files",{'file':file,"lawyers":lawyers,"images": images,'file_fee':file_fee,})
   
    return render(request,"files/file_fees.html",{'file_fee':file_fee,'file':file,'form':form,"lawyers":lawyers,"images": images,} )



 
# FILE DELETE VIEW
# class FileDeleteView(LoginRequiredMixin, generic.DeleteView):
#     template_name = "files/file_delete.html"
#     queryset = File.objects.all()

#     def get_success_url(self):
#         parent_dir2 = settings.MEDIA_ROOT+"\\class\\" + str(pk)
#         for i in os.listdir(parent_dir2):
#                 os.remove( settings.MEDIA_ROOT + "/class/"+ str(pk)+ "/" +i)
#         return reverse("files:file-list")


def file_delete(request, pk):
    file = File.objects.get(id=pk)
    if request.method == "POST":
        
        file.delete()
        path = settings.MEDIA_ROOT+"\\class\\" + str(pk)
        for i in os.listdir(path):
                os.remove( settings.MEDIA_ROOT + "/class/"+ str(pk)+ "/" +i)
        return redirect("/files")
    return render(request,"files/file_delete.html",{'file':file} )









def FileDeleteUpdate(request):
    lawyer=Lawyer.objects.filter(user=request.user).first()
    file_array = json.loads(request.body)
    print(file_array)
    for i in file_array["file_array"]:   
        image= Image.objects.filter(id = i)
        img= Image.objects.filter(id = i).first()
        print(img.image)
        # # path = settings.MEDIA_ROOT+ img.image
        os.remove( settings.MEDIA_ROOT + "\\" + str(img.image))
        file= File.objects.filter(id=image[0].file_name.id)
        file.update(lawyer=lawyer)
        image.delete()
    return JsonResponse('Payment submitted..', safe=False)