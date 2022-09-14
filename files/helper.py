import os
from .models import File,Image
from django.conf import settings
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.http import HttpResponse, HttpResponseRedirect, request
def user_passes_test_helper(
    test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME
):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc
            ):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            return  HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        return _wrapped_view

    return decorator

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



