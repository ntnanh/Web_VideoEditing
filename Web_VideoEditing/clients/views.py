from django.shortcuts import render
from users.models import Users
from django.http import HttpResponse
import os
from django.conf import settings
from .forms import FileUploadForm
from users.views import base_context
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

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
    if request.method == 'POST':
        starttime = request.POST.get('start')
        endtime = request.POST.get('end')

        input_video_path = '/static/clients/images/video1.mp4'
        output_video_path = '/static/clients/images/input_video1.mp4'
        if starttime and endtime:
            start_time_seconds = convert_to_seconds(starttime)
            end_time_seconds = convert_to_seconds(endtime)

            ffmpeg_extract_subclip(input_video_path, start_time_seconds, end_time_seconds, targetname=output_video_path)

            video_url = '/static/appcut/images/input_video1.mp4'
            return render(request, "clients/cut_tool.html", {'video_url': video_url})

    return render(request, "clients/cut_tool.html")

def convert_to_seconds(time_string):
    hours, minutes, seconds = map(int, time_string.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def loop_video(request):
    context = base_context(request)
    return render(request, 'clients/loop_video.html', context)

def loop_tool(request):
    return render(request, 'clients/loop_tool.html')
