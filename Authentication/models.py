from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="user_profile", null=True, blank=True)
    department_code = models.CharField(max_length=10,default="CSE")
    semester = models.IntegerField(default=1)
    phone = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    aproved_status = models.BooleanField(default=False)

    tweter_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.email
    
