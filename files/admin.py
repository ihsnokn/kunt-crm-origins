from django.contrib import admin

from .models import Image, User, File, Lawyer, UserProfile,File_Notes

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(File)
admin.site.register(Lawyer)
admin.site.register(File_Notes)


admin.site.register(Image)
