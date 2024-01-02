from django.shortcuts import render, redirect
from django.urls import reverse
from users.models import Users
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from .forms import FileUploadForm
from users.views import base_context
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, vfx, concatenate_videoclips
from .models import Upload,UserUpload

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
    context = base_context(request)
    if request.method == 'POST' and 'video_file' in request.FILES:
        video_file = request.FILES['video_file']
        title = video_file.name
        upload = Upload(path_video=video_file, title_video=title, path_image='')
        upload.save()
        upload_id = upload.id
        user_upload = UserUpload(upload_id=upload_id, user_id=request.session.get('user_id'))
        user_upload.save()
        redirect_url = reverse('clients:cut_tool', kwargs={'id': upload_id})
        return redirect(redirect_url)
    else:
        return render(request, 'clients/cut_video.html', context)

def preview_cut_video(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        upload = Upload.objects.get(id=id)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        input_video_path = request.POST.get('video_path')
        output_video_path = os.path.join(settings.BASE_DIR, f"media/Files/previews/output_preview.mp4")
        if start_time and end_time:
            start_time_seconds = convert_to_seconds(start_time)
            end_time_seconds = convert_to_seconds(end_time)
            ffmpeg_extract_subclip(input_video_path, start_time_seconds, end_time_seconds, targetname=output_video_path)
            preview_video = f"/media/Files/previews/output_preview.mp4"
            return JsonResponse({'preview_video' : preview_video})
        content = {
            'id': id,
            'video_url': upload.path_video.url,
            'full_path': upload.path_video.path
        }
        return render(request, "clients/cut_tool.html", content)

def cut_tool(request, id):
    upload = Upload.objects.get(id=id)
    if request.method == 'POST':
        starttime = request.POST.get('start')
        endtime = request.POST.get('end')
        input_video_path = request.POST.get('full_path')
        output_video_path = 'D:\Web_VideoEditing\web_videoediting\media\Files\input_video1.mp4'
        if starttime and endtime:
            start_time_seconds = convert_to_seconds(starttime)
            end_time_seconds = convert_to_seconds(endtime)

            ffmpeg_extract_subclip(input_video_path, start_time_seconds, end_time_seconds, targetname=output_video_path)

            video_url = '/media/Files/input_video1.mp4'
            content = {
                'id': id,
                'preview_video': video_url,
                'video_url': upload.path_video.url,
                'full_path': upload.path_video.path
                }
            return render(request, "clients/cut_tool.html", content)
    return render(request, "clients/cut_tool.html", {'id':id,'video_url': upload.path_video.url, 'full_path': upload.path_video.path})

def convert_to_seconds(time_string):
    hours, minutes, seconds = map(int, time_string.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def loop_video(request):
    context = base_context(request)
    if request.method == 'POST' and 'video_file' in request.FILES:
        video_file = request.FILES['video_file']
        title = video_file.name
        upload = Upload(path_video=video_file, title_video=title, path_image='')
        upload.save()
        upload_id = upload.id
        user_upload = UserUpload(upload_id=upload_id, user_id=request.session.get('user_id'))
        user_upload.save()
        redirect_url = reverse('clients:loop_tool', kwargs={'id': upload_id})
        return redirect(redirect_url)
    else:
        return render(request, 'clients/loop_video.html', context)

from django.conf import settings
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def loop_tool(request, id):
    upload = Upload.objects.get(id=id)
    preview_video = upload.path_video.url  # Đường dẫn mặc định là video gốc chưa được lặp lại

    if request.method == 'POST':
        video_path = request.POST.get('full_path')
        loop_factor = 1 
        loop_factor_values = request.POST.getlist('loop_factor')
        if '2x' in loop_factor_values:
            loop_factor = 2
        elif '3x' in loop_factor_values:
            loop_factor = 3
        elif '4x' in loop_factor_values:
            loop_factor = 4
        elif '5x' in loop_factor_values:
            loop_factor = 5

        clip = VideoFileClip(video_path)
        clips = [clip.copy() for _ in range(loop_factor)]
        final_clip = concatenate_videoclips(clips)

        looped_video_path = os.path.join(settings.MEDIA_ROOT, 'inputloopvideo.mp4')
        final_clip.write_videofile(looped_video_path)

        preview_video = looped_video_path 
        # Gán đường dẫn của video đã lặp lại cho biến preview_video
        
        
        
        looped_video_path = os.path.join(settings.MEDIA_ROOT, 'inputloopvideo.mp4')
        final_clip.write_videofile(looped_video_path)
        preview_video = os.path.join(settings.MEDIA_URL, 'inputloopvideo.mp4')

        print("Original video path:", upload.path_video.url)
        print("Looped video path:", preview_video)
        print("Video factor:", loop_factor)
        print("Original video duration:", clip.duration)
        print("Looped video duration:", final_clip.duration)


    return render(request, "clients/loop_tool.html", {'id': id, 'video_url': upload.path_video.url, 'full_path': upload.path_video.path, 'preview_video': preview_video})

def loop_input(video_path, loop_factor):
    
    clip = VideoFileClip(video_path)
    clips = [clip.copy() for _ in range(loop_factor)]
    # Concatenate the replicated clips to create the final looped video
    final_clip = concatenate_videoclips(clips)

    final_clip.write_videofile("media/Files/inputloopvideo.mp4")