from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random
from django.core.mail import send_mail

from Authentication.models import CustomUser

# Create your views here.

class UserRegister(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.is_superuser:
            cp={
                "active_id":"a001",
            }
            return render(request, "register.html", context=cp)

        else:
            return redirect("/")
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        if user.is_superuser:
            data = request.POST

            if CustomUser.objects.filter(email=data['email']).exists():
                cp = {
                    'icon':'warning',
                    'title':"User Already Exists!",
                    'text': "The user with this email already exists in the database!"
                }
                return render(request,'alarts.html', context=cp)
            elif CustomUser.objects.filter(username=data['username']).exists():
                cp = {
                    'icon':'warning',
                    'title':"User Already Exists!",
                    'text': "The user with this username already exists in the database!"
                }
                return render(request,'alarts.html', context=cp)
            elif data.get('password1') != data.get('password2'):

                cp = {
                    'icon':'warning',
                    'title':"Password Mismatch!",
                    'text': "The password and confirm password doesn't match!"
                }
                return render(request,'alarts.html', context=cp)
            else:
                users = CustomUser.objects.create(                    
                    email=data.get('email'),
                    username=data.get('username'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    department_code=data.get('department_code').upper(),
                    
                )
                
                users.set_password(data.get('password1'))
                users.save()
               
                cp = {
                    'icon':'success',
                    'title':"User Created Successfully!",
                    'text': "The user has been created successfully!"
                }
                return render(request,'alarts.html', context=cp)


        else:
            cp = {
                'icon':'error',
                'title':"You can't access this page!",
                'text': "Ensure you are the admin of the website!"
            }
            return render(request,'alarts.html', context=cp)

class UserLogin(View):
    def get(self, request):

        return render(request, "login.html")
      
    def post(self,request):
        method = request.POST.get('_method', '').upper()
        if method == 'EMAILVERYFI':
            email =request.POST.get('email')
            users = CustomUser.objects.filter(email = email)[0]
            otp = request.POST.get('otp')
            if users.otp == otp:
                users.is_email_verified = True
                users.save()
                login(request,users)
                return redirect('/')
            
        data = request.POST
        username = data.get('username')
        pasword = data.get('password')
        loginuser = authenticate(request,username=username,password=pasword)

        if loginuser is not None:
            
            if loginuser.is_email_verified == True:
                login(request,loginuser)
                return redirect('/')
            else:
                email = loginuser.email 
                otp = random.randint(0,999999)
                send_mail(
                    "Your OTP is",
                    f"Your email Verification otp : {otp}",
                    'from@gmail.com',
                    [email],
                    
                    )
                loginuser.otp = otp
                loginuser.save()

                cp = {
                    'email':email,
                    
                }
                return render (request, 'modal.html', context=cp)
        else:


            cp = {
                'icon':'warning',
                'title':"Invailed Username or Password!",
                'text': "Ensure Username or Password is Currect!"
            }
            return render(request,'alarts.html', context=cp)    
            

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/')
    



########### Users ########### Management ###########

class Users(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        if user.is_superuser:
            users = CustomUser.objects.all()
            students = CustomUser.objects.filter(is_student = True)
            teachers = CustomUser.objects.filter(is_teacher = True)
            cp = {
                "active_id":"a002",
                'students':students,
                'teachers':teachers,
                "users":users,
                
            }
            return render(request, "users.html", context=cp)

        else:
            return redirect("/")
