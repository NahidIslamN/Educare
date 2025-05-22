from django.contrib import admin

# Register your models here.


from django.contrib import admin
from Authentication.models import *
from django.contrib.auth.admin import UserAdmin




admin.site.register(CustomUser)

