import os
from .models import File,Image
from django.conf import settings

def classification_helper(name,files,form,lawyer):
       
        file = form.save(commit=False)
        file.lawyer=lawyer
        file.save()

        file_name = File.objects.filter(id=file.id).first()
    
        for file in files:
            deneme= Image.objects.create(file_name=file_name, image=file)
            deneme.save()
            initial_path = deneme.image.path
            print(initial_path)
            directory = str(file_name.id)
            print(directory)
            parent_dir = settings.MEDIA_ROOT +"//class" ## windows için \\ 
            path = os.path.join(parent_dir, directory)
            print(path)
            x = str(deneme.image).split("/")
            print(x)
            if not os.path.exists(path):
                os.mkdir(path)
            new_path = settings.MEDIA_ROOT + "//" + x[0] + "//"  +  str(file_name.id)  + "//" + x[-1]  ## windows için \\
            print(new_path) 
            print(x[0] + "//"  +  str(file_name.id)  + "//" + x[-1])  ## windows için \\ 
            link_path=x[0] + "//"  +  str(file_name.id)  + "//" + x[-1]  ## windows için \\ 
            print(link_path) 
            os.replace(initial_path, new_path)
            deneme.image = link_path 
            deneme.save()
            
