
from django.urls import path
from Authentication.views import *




urlpatterns = [    
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('users/', Users.as_view(), name='users'),
]
