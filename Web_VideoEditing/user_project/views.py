from django.shortcuts import render
from users.models import Users
from django.http import HttpResponse
from django.urls import reverse
from users.views import base_context

# Create your views here.

def home(request):
    context = base_context(request)
    return render(request, 'user_project/index.html', context)

def forgot_password(request):
    return render(request, 'user_project/forgot_password.html')
