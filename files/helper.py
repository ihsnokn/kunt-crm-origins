import os
from .models import File,Image
from django.conf import settings

def classification_helper(files,form,lawyer,update):       
        file_1 = form.save(commit=False)
        file_1.lawyer=lawyer
        file_1.save()
        file_name = File.objects.filter(id=file_1.id).first()   
        for file in files:
            if (len(file.name) > 180):
                if (update != True):                
                    file_1.delete()               
                print(len(file.name))
                return False
            deneme= Image.objects.create(file_name=file_name, image=file)
            deneme.save()
            initial_path = deneme.image.path
            directory = str(file_name.id)
            parent_dir = settings.MEDIA_ROOT +"//class" ## windows için \\ 
            path = os.path.join(parent_dir, directory)
            x = str(deneme.image).split("/")
            if not os.path.exists(path):
                os.mkdir(path)
            new_path = settings.MEDIA_ROOT + "//" + x[0] + "//"  +  str(file_name.id)  + "//" + x[-1]  ## windows için \\
            link_path=x[0] + "//"  +  str(file_name.id)  + "//" + x[-1]  ## windows için \\ 
            os.replace(initial_path, new_path)
            deneme.image = link_path 
            deneme.save()
