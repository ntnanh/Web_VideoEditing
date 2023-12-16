from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Users

def home(request):
    return render(request, 'users/index.html')

def signup(request):
    return render(request, 'users/signup.html')

def postSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mysqluser = Users(username=username, email=email, password=password)
        mysqluser.save()

        messages.success(request, 'Đăng ký thành công!')

        return render(request, 'users/signin.html')
    
    return HttpResponseBadRequest('Bad Request: Only POST requests are allowed.')
    
def signin(request):
    return render(request, 'users/signin.html')

def postSignin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Users.empAuth_objects.get(email=email, password=password)
            if user is not None:
                return render(request, 'users/index.html')
            else:
                print("Some tried to login and failed")
                print("They used email: {} and password: {}".format(email, password))
                
                return redirect('/')
        except Exception as identifier:
            return redirect("/")
    else:
        return render(request, 'users/signin.html')
    
def signout(request):
    pass