from django.shortcuts import render
from users.models import Users
from django.http import HttpResponse
import os
from django.conf import settings
from .forms import FileUploadForm

def base_context(request):
    username = request.session.get('username', None)
    user_profile = Users.objects.get(username=username) if username else None
    return {'user_profile': user_profile}

def home(request):
    context = base_context(request)
    return render(request, 'clients/index.html', context)

def all_tools(request):
    context = base_context(request)
    return render(request, 'clients/all_tools.html', context)


def add_subtitles(request):
    return render(request, 'clients/add_subtitles.html')

def merge_video(request):
    context = base_context(request)
    return render(request, 'clients/merge_video.html', context)

def merge_tools(request):
    return render(request, 'clients/merge_tools.html')

def crop_video(request):
    context = base_context(request)
    return render(request, 'clients/crop_video.html', context)

def crop_tool(request):
    return render(request, 'clients/crop_tool.html')

def cut_video(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        dd(form.is_valid())
        if form.is_valid():
            dd(form)
    else:
        form = FileUploadForm()
        
    context = base_context(request)
    return render(request, 'clients/cut_video.html', context)

def cut_tool(request):
    return render(request, 'clients/cut_tool.html')

def loop_video(request):
    context = base_context(request)
    return render(request, 'clients/loop_video.html', context)

def loop_tool(request):
    return render(request, 'clients/loop_tool.html')
