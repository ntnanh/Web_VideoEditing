from django.shortcuts import render
from users.models import Users
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def base_context(request):
    username = request.session.get('username', None)
    user_profile = Users.objects.get(username=username) if username else None
    return {'user_profile': user_profile}

def home(request):
    context = base_context(request)
    return render(request, 'user_project/index.html', context)

def forgot_password(request):
    return render(request, 'user_project/forgot_password.html')
