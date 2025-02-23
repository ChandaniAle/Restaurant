from django.contrib import admin
from .models import formcontainer

# Register your models here.
class Adminformcontainer(admin.ModelAdmin):
    list_display=['id', 'name', 'email', 'phone_number']
    
admin.site.register(formcontainer,Adminformcontainer)

    

