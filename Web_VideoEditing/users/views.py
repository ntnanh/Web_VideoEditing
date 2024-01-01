
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib import messages
from .models import Users
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # check username
        if Users.objects.filter(username=username).exists():
            error_message = '**Username already exists.'
            return JsonResponse({'error_message': error_message})
        
        # Kiểm tra email và tính hợp lệ của email
        try:
            Users.objects.get(email=email)
            email_message = '**Email already exists.'
            return JsonResponse({'email_message': email_message})
        except Users.DoesNotExist:
            try:
                validate_email(email)
            except ValidationError:
                email_message = '**Invalid email.'
                return JsonResponse({'email_message': email_message})
        
        #check password least 8 characters
        if len(password) < 8:
            password_message = '**Password must be at least 8 characters long.'
            return JsonResponse({'password_message': password_message})
        
        hashed_password = make_password(password)
        mysqluser = Users(username=username, email=email, password=hashed_password)
        mysqluser.save()
        
        return redirect('users:signin')

    return render(request, 'users/signup.html')

def signin(request):
    error_message = None  # Biến lưu trữ thông báo lỗi

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(email=email)
            if check_password(password,user.password) and user is not None:
                request.session['username'] = user.username
                if user.role == 'admin':
                    return redirect('administrators:index')
                elif user.role == 'client':
                    return redirect('clients:home')
                
            else:
                error_message = "Email or password is incorrect."  # Gán thông báo lỗi
                
                print("Someone tried to login and failed")
                print("They used email: {} and password: {}".format(email, password))
                
                return render(request, 'users/signin.html', {'error_message': error_message})
        except Users.DoesNotExist:
            error_message = "User does not exist."  # Gán thông báo lỗi
            
            print("User does not exist")
            
            return render(request, 'users/signin.html', {'error_message': error_message})
    
    return render(request, 'users/signin.html', {'error_message': error_message})
    
def base_context(request):
    username = request.session.get('username', None)
    user_profile = Users.objects.get(username=username) if username else None
    return {'user_profile': user_profile}

def signout(request):
    logout(request)
    return redirect('clients:home')