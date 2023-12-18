from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Users

def home(request):
    username = request.session.get('username', None)
    return render(request, 'users/index.html', {'username': username})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mysqluser = Users(username=username, email=email, password=password)
        mysqluser.save()

        messages.success(request, 'Đăng ký thành công!')

        return render(request, 'users/signin.html')
    
    # return HttpResponseBadRequest('Bad Request: Only POST requests are allowed.')
    
    return render(request, 'users/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Users.empAuth_objects.get(email=email, password=password)
            if user is not None:
                request.session['username'] = user.username
                return redirect('home')
            else:
                print("Some tried to login and failed")
                print("They used email: {} and password: {}".format(email, password))
                
                return redirect('/')
        except Users.DoesNotExist:
            print("User does not exist")
            return redirect("/")
    
    return render(request, 'users/signin.html')
    
def signout(request):
    pass