from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Users

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        mysqluser = Users(username=username, email=email, password=password)
        mysqluser.save()
        return redirect('signin')
    
    
    return render(request, 'users/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Users.objects.get(email=email, password=password)
            if user is not None:
                request.session['username'] = user.username
                return redirect('clients:home')
            else:
                print("Some tried to login and failed")
                print("They used email: {} and password: {}".format(email, password))
                
                return redirect('/')
        except Users.DoesNotExist:
            print("User does not exist")
            return redirect("/")
    
    return render(request, 'users/signin.html')
    
def signout(request):
    logout(request)
    return redirect('clients:home')