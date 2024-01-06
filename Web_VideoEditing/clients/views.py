from django.shortcuts import render, redirect
from django.urls import reverse
from users.models import Users
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from .forms import FileUploadForm
from users.views import base_context
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from .models import Upload,UserUpload
from .models import Upload,UserUpload, Video, Subtitle
import uuid
from moviepy.editor import VideoFileClip, vfx, AudioFileClip, concatenate_audioclips
from datetime import datetime
from pydub import AudioSegment
import re
import time
import requests

def home(request):
    context = base_context(request)
    return render(request, 'clients/index.html', context)

def all_tools(request):
    context = base_context(request)
    return render(request, 'clients/all_tools.html', context)


def add_voice(request):
    context = base_context(request)
    if request.method == 'POST' and 'video_file' in request.FILES:
        if request.session.get('user_id') is None:
            return redirect('users:signin')
        video_file = request.FILES['video_file']
        title = video_file.name
        upload = Upload(path_video=video_file, title_video=title, path_image='')
        upload.save()
        upload_id = upload.id
        user_upload = UserUpload(upload_id=upload_id, user_id=request.session.get('user_id'))
        user_upload.save()
        redirect_url = reverse('clients:add_voice_tool', kwargs={'id': upload_id})
        return redirect(redirect_url)
    else:
        return render(request, 'clients/add_voice.html', context)

def upload_subtitle(request):
    context = base_context(request)
    if request.method == 'POST' and 'sub_file' in request.FILES:
        sub_file = request.FILES['sub_file']
        path_file = os.path.join(settings.BASE_DIR, f"media/Files/{sub_file.name}")
        # Save the uploaded file to the specified location
        with open(path_file, 'wb') as file_destination:
            for chunk in sub_file.chunks():
                file_destination.write(chunk)
        return JsonResponse({'path_sub' : path_file})
    else:
        return render(request, 'clients/add_voice.html', context)

def preview_voice_to_video(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        upload = Upload.objects.get(id=id)
        input_video_path = request.POST.get('video_path')
        path_sub = request.POST.get('path_sub')
        final_video = handle_sub(input_video_path, path_sub)
        return JsonResponse({'preview_video' : final_video})

def handle_sub(path_video, path_sub):
    video_clip = VideoFileClip(path_video)
    output_audio_file = os.path.join(settings.BASE_DIR, 'media/Files/output_audio.mp3')
    final_video = os.path.join(settings.BASE_DIR, 'media/Files/previews/output.mp4')
    video_file = path_video
    # Phân tích tệp SRT
    with open(path_sub, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()
    audio_clips = []
    count = 0
    # Tạo audio cho từng phụ đề và đồng bộ hóa với video
    for i in range(0, len(srt_lines), 4):
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text = srt_lines[i + 2].strip()
            url = 'https://api.fpt.ai/hmi/tts/v5'
            payload = text
            headers = {
                'api-key': 'abAl9piv7XGwHVn5onzLLzTrNGbh5LPZ',
                'speed': '',
                'voice': 'banmai'
            }

            response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                print(text)
                audio_url = response_data.get('async')

                # Tải tệp âm thanh đã tạo từ URL
                audio_response = requests.get(audio_url)
                if audio_response.status_code == 200:
                    with open(output_audio_file, 'wb') as audio_file:
                        audio_file.write(audio_response.content)
                        audio_clip = AudioSegment.from_file(output_audio_file)
                        adjusted_audio = audio_clip._spawn(audio_clip.raw_data, overrides={
                            "frame_rate": int(audio_clip.frame_rate * 1)
                        }).set_frame_rate(audio_clip.frame_rate)
                        adjusted_audio.export("adjusted_audio.mp3", format="mp3")
                        audio_export = AudioFileClip("adjusted_audio.mp3")
                        audio_clips.append(audio_export)
            else:
                print(response.json())
            time.sleep(1)
    # Kết hợp (merge) các audio trong danh sách
    merged_audio = concatenate_audioclips(audio_clips)
    # Lưu âm thanh kết hợp thành tệp mới
    merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
    merged_audio = AudioFileClip("merged_audio.mp3")
    audio_duration = merged_audio.duration
    new_video = video_clip.set_duration(audio_duration)
    video_with_new_audio = new_video.set_audio(merged_audio)
    video_with_new_audio.write_videofile(final_video, codec='libx264', audio_codec='aac')
    os.remove(path_sub)
    os.remove(path_video)
    os.remove(output_audio_file)

    return '/media/Files/previews/output.mp4'

def is_valid_time_format(time_str):
    # Định dạng thời gian "HH:MM:SS,sss --> HH:MM:SS,sss" (giờ, phút, giây, mili-giây)
    time_format = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
    return bool(re.match(time_format, time_str))

def add_voice_tool(request, id):
    upload = Upload.objects.get(id=id)
    return render(request, "clients/add_voice_tool.html", {'id':id,'video_url': upload.path_video.url, 'full_path': upload.path_video.path})

# def merge_video(request):
#     context = base_context(request)
#     return render(request, 'clients/merge_video.html', context)

def merge_video(request):
    context = base_context(request)
    if request.method == 'POST' and 'video_file' in request.FILES:
        video_file = request.FILES['video_file']
        title = video_file.name
        upload = Upload(path_video=video_file, title_video=title, path_image='')
        upload.save()
        upload_id = upload.id
        user_upload = UserUpload(upload_id=upload_id, user_id=request.session.get('user_id'))
        user_upload.save()
        redirect_url = reverse('clients:merge_tools', kwargs={'id': upload_id})
        return redirect(redirect_url)
    else:
        return render(request, 'clients/merge_video.html', context)



# def merge_tools(request):
#     return render(request, 'clients/merge_tools.html')


def merge_tools(request, id):
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
            return render(request, "clients/merge_tools.html", content)
    return render(request, "clients/merge_tools.html", {'id':id,'video_url': upload.path_video.url, 'full_path': upload.path_video.path})


def crop_video(request):
    context = base_context(request)
    return render(request, 'clients/crop_video.html', context)

def crop_tool(request):
    return render(request, 'clients/crop_tool.html')

def add_subtitles_tool(request):
    return render(request, 'clients/add_subtitles_tool.html')

def cut_video(request):
    context = base_context(request)
    if request.method == 'POST' and 'video_file' in request.FILES:
        if request.session.get('user_id') is None:
            return redirect('users:signin')
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
        output_video_path = os.path.join(settings.BASE_DIR, f"media/Files/previews/output_preview_{id}.mp4")
        if start_time and end_time:
            start_time_seconds = convert_to_seconds(start_time)
            end_time_seconds = convert_to_seconds(end_time)
            ffmpeg_extract_subclip(input_video_path, start_time_seconds, end_time_seconds, targetname=output_video_path)
            preview_video = f"/media/Files/previews/output_preview_{id}.mp4"
            return JsonResponse({'preview_video' : preview_video})
        content = {
            'id': id,
            'video_url': upload.path_video.url,
            'full_path': upload.path_video.path
        }
        return render(request, "clients/cut_tool.html", content)

def export_cut_video(request):
    url = request.POST.get('url').replace('/', '', 1)
    id = request.POST.get('id')
    local_video = os.path.join(settings.BASE_DIR, url)
    unique_id = str(uuid.uuid4()).split('-')[-1]
    file_name = f"downloaded_file_{unique_id}_{id}.mp4"
    dir_download = os.path.join(settings.BASE_DIR, f"media/Files/exports/{file_name}")
    with open(local_video, 'rb') as file:
        with open(dir_download, 'wb') as downloaded_file:
            chunk = file.read(1024)  # Read the file in chunks of 1024 bytes
            while chunk:
                downloaded_file.write(chunk)  # Write the chunk to the new file
                chunk = file.read(1024)  # Read the next chunk
    # Handle get data save video table
    clip = VideoFileClip(dir_download)
    duration = clip.duration
    file_size = os.path.getsize(dir_download)
    file_extension = os.path.splitext(dir_download)[1]
    file_format = file_extension[1:]  # Removing the dot from the extension
    current_date = datetime.now().date()
    # Save file to Upload table
    upload = Upload(path_video=f"Files/exports/{file_name}", title_video=file_name, path_image='')
    upload.save()
    # Save file to UserUpload table
    user_upload = UserUpload(upload_id=upload.id, user_id=request.session.get('user_id'))
    user_upload.save()
    # Save file to Video table
    video = Video(title=file_name, video_edit=file_name, duration=duration, format=file_format, size=file_size, update_date=current_date, thumb='', upload_id_id=upload.id, user_id_id=request.session.get('user_id'))
    video.save()

    return JsonResponse({'success' : 'true'})

def cut_tool(request, id):
    upload = Upload.objects.get(id=id)
    return render(request, "clients/cut_tool.html", {'id':id,'video_url': upload.path_video.url, 'full_path': upload.path_video.path})

def convert_to_seconds(time_string):
    hours, minutes, seconds = map(int, time_string.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def loop_video(request):
    context = base_context(request)
    if request.method == 'POST' and 'video_file' in request.FILES:
        if request.session.get('user_id') is None:
            return redirect('users:signin')
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
        loop_factor_values = request.POST.get('loop')
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
        return JsonResponse({'preview_video' : preview_video})
    return render(request, "clients/loop_tool.html", {'id': id, 'video_url': upload.path_video.url, 'full_path': upload.path_video.path, 'preview_video': preview_video})

def export_loop_video(request):
    url = request.POST.get('url').replace('/', '', 1)
    id = request.POST.get('id')
    local_video = os.path.join(settings.BASE_DIR, url)
    unique_id = str(uuid.uuid4()).split('-')[-1]
    file_name = f"downloaded_file_{unique_id}_{id}.mp4"
    dir_download = os.path.join(settings.BASE_DIR, f"media/Files/exports/{file_name}")
    with open(local_video, 'rb') as file:
        with open(dir_download, 'wb') as downloaded_file:
            chunk = file.read(1024)  # Read the file in chunks of 1024 bytes
            while chunk:
                downloaded_file.write(chunk)  # Write the chunk to the new file
                chunk = file.read(1024)  # Read the next chunk
    # Handle get data save video table
    clip = VideoFileClip(dir_download)
    duration = clip.duration
    file_size = os.path.getsize(dir_download)
    file_extension = os.path.splitext(dir_download)[1]
    file_format = file_extension[1:]  # Removing the dot from the extension
    current_date = datetime.now().date()
    # Save file to Upload table
    upload = Upload(path_video=f"Files/exports/{file_name}", title_video=file_name, path_image='')
    upload.save()
    # Save file to UserUpload table
    user_upload = UserUpload(upload_id=upload.id, user_id=request.session.get('user_id'))
    user_upload.save()
    # Save file to Video table
    video = Video(title=file_name, video_edit=file_name, duration=duration, format=file_format, size=file_size, update_date=current_date, thumb='', upload_id_id=upload.id, user_id_id=request.session.get('user_id'))
    video.save()

    return JsonResponse({'success' : 'true'})

def loop_input(video_path, loop_factor):
    
    clip = VideoFileClip(video_path)
    clips = [clip.copy() for _ in range(loop_factor)]
    # Concatenate the replicated clips to create the final looped video
    final_clip = concatenate_videoclips(clips)

    final_clip.write_videofile("media/Files/inputloopvideo.mp4")