from django.shortcuts import render, redirect
from users.models import Users
from django.http import HttpResponse
from django.urls import reverse
from users.views import base_context

# Create your views here.
def check_user_role(request):
    if 'username' not in request.session:
        return redirect('users:signin')
    
    username = request.session.get('username', None)
    user_profile = Users.objects.get(username=username) if username else None
    
    if user_profile.role == 'admin':
        return redirect('administrators:index')
    
    return None

def home(request, id):
    context = base_context(request)
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    return render(request, 'user_project/index.html', context)

def forgot_password(request):
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    return render(request, 'user_project/forgot_password.html')


def profile(request):
    return render(request, 'user_project/profile.html')
