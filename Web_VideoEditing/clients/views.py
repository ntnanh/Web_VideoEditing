from django.shortcuts import render, redirect
from django.urls import reverse
from users.models import Users
from django.http import HttpResponse, JsonResponse
import os
import json
from django.conf import settings
from .forms import FileUploadForm
from users.views import base_context
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from .models import Upload,UserUpload
from .models import Upload,UserUpload, Video, Subtitle
import uuid
from moviepy.editor import VideoFileClip, vfx, AudioFileClip, concatenate_audioclips, concatenate_videoclips, TextClip, CompositeVideoClip, VideoClip
from datetime import datetime
from pydub import AudioSegment
import re
import time
import requests
import subprocess
import json

def home(request):
    context = base_context(request)
    return render(request, 'clients/index.html', context)

def all_tools(request):
    context = base_context(request)
    return render(request, 'clients/all_tools.html', context)

def subtitle_video(request):
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
        redirect_url = reverse('clients:subtitle', kwargs={'id': upload_id})
        return redirect(redirect_url)
    else:
        return render(request, 'clients/add_subtitles.html', context)

def add_subtitles_tool(request, id, subtitle_id):
    upload = Upload.objects.get(id=id)
    subtitle = Subtitle.objects.get(id=subtitle_id)
    if subtitle.path.path is not None:
        subtitles = detect_subtitle(subtitle.path.path)
    data = {
        'id':id,
        'video_url': upload.path_video.url,
        'full_path': upload.path_video.path,
        'subtitles': subtitles
    }

    return render(request, "clients/add_subtitle_tool.html", data)

def detect_subtitle(path):
    with open(path, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()
    subtitles = []
    for i in range(0, len(srt_lines), 4):
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text = srt_lines[i + 2].strip()
            subtitle = {
                'start_time': format_time(start_time),
                'end_time': format_time(end_time),
                'text': text
            }
            subtitles.append(subtitle)
    return subtitles
    # Kết hợp (merge) các audio trong danh sách
def preview_add_subtitles(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        upload = Upload.objects.get(id=id)
        input_video_path = request.POST.get('video_path')
        video = VideoFileClip(upload.path_video.path)
        final_video = os.path.join(settings.BASE_DIR, 'media/Files/previews/output.mp4')
        subtitles = request.POST.get('subtitles')
        subtitles = json.loads(subtitles)
        video_clips = sub_clips = []
        for sub in subtitles:
            start_time = format_time_to_seconds(sub["start_time"])
            end_time = format_time_to_seconds(sub["end_time"])
            videoClip = video.subclip(start_time, end_time)
            text = sub["text"]
            font_size = int(min(video.size) / 20)
            # Insert line breaks based on video width and maximum characters per line
            max_chars_per_line = int(video.size[0] / font_size)
            text_with_line_breaks = insert_line_breaks(text, max_chars_per_line)
            subtitle_clip = generate_subtitle(text_with_line_breaks, start_time , end_time, font_size)
            sub_clips.append(subtitle_clip)
        video_with_subtitles = CompositeVideoClip([video] + sub_clips)
        video_with_subtitles.write_videofile(final_video, codec="libx264", audio_codec="aac",fps=24)


        return JsonResponse({'preview_video' : '/media/Files/previews/output.mp4'})
# Function to insert line breaks in text based on width
def insert_line_breaks(text, max_chars):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word

    lines.append(current_line.strip())
    return "\n".join(lines)

def format_time_to_seconds(time):
# Split the time string into minutes, seconds, and milliseconds
    minutes, seconds = map(float, time.split(':'))

    # Convert the time to seconds
    total_seconds = (minutes * 60) + seconds
    return total_seconds

def generate_subtitle(subtitle_text, start_time, end_time, font_size):
    duration = end_time - start_time
    textClip = TextClip(subtitle_text, fontsize=font_size, font='Arial', color='white', bg_color='black')
    # Calculate the desired padding (in pixels)
    padding_x = 20  # Horizontal padding
    padding_y = 20  # Vertical padding

    # Increase the size of the text clip to add padding
    textClip = textClip.margin(left=padding_x, right=padding_x, top=padding_y, bottom=padding_y)
    textClip = textClip.set_start(start_time).set_end(end_time).set_duration(duration).set_position(("center", "bottom"))
    return textClip

def format_time(time):
    # Parse the input time string
    time_obj = datetime.strptime(time, '%H:%M:%S,%f')
    # Calculate total seconds with microseconds truncated to two decimal places
    total_seconds = time_obj.second + (time_obj.microsecond / 10**6)
    formatted_time = f"{time_obj.minute:02}:0{total_seconds:.2f}"
    return formatted_time

def subtitle(request, id):
    context = base_context(request)
    if request.method == 'POST' and 'sub_file' in request.FILES:
        if request.session.get('user_id') is None:
            return redirect('users:signin')
        sub_file = request.FILES['sub_file']
        path_file = os.path.join(settings.BASE_DIR, f"media/Files/{sub_file.name}")
        name = sub_file.name
        subtitle = Subtitle(path=sub_file, name=name)
        subtitle.save()
        subtitle_id = subtitle.id
        redirect_url = reverse('clients:add_subtitles_tool', kwargs={'id': id,'subtitle_id':subtitle_id})
        return redirect(redirect_url)

    return render(request, "clients/subtitle.html", {'id':id})

def subtitle_voice(request, id):
    context = base_context(request)
    if request.method == 'POST' and 'sub_file' in request.FILES:
        if request.session.get('user_id') is None:
            return redirect('users:signin')
        sub_file = request.FILES['sub_file']
        path_file = os.path.join(settings.BASE_DIR, f"media/Files/{sub_file.name}")
        name = sub_file.name
        subtitle = Subtitle(path=sub_file, name=name)
        subtitle.save()
        subtitle_id = subtitle.id
        redirect_url = reverse('clients:add_voice_tool', kwargs={'id': id,'subtitle_id':subtitle_id})
        return redirect(redirect_url)

    return render(request, "clients/subtitle_voice.html", {'id':id})

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
        redirect_url = reverse('clients:subtitle_voice', kwargs={'id': upload_id})
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
        final_video = os.path.join(settings.BASE_DIR, 'media/Files/previews/output.mp4')
        subtitles = request.POST.get('subtitles')
        subtitles = json.loads(subtitles)
        final_video = handle_sub(input_video_path, subtitles)
        return JsonResponse({'preview_video' : final_video})

def handle_sub(path_video, subtitles):
    video_clip = VideoFileClip(path_video)
    output_audio_file = os.path.join(settings.BASE_DIR, 'media/Files/output_audio.mp3')
    final_video = os.path.join(settings.BASE_DIR,'media\Files\previews\output.mp4')
    video_file = path_video
    audio_clips = []
    for sub in subtitles:
        start_time = format_time_to_seconds(sub["start_time"])
        end_time = format_time_to_seconds(sub["end_time"])
        videoClip = video_clip.subclip(start_time, end_time)
        text = sub["text"]
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
            audio_url = response_data.get('async')
            # Tải tệp âm thanh đã tạo từ URL
            max_retries = 4
            for retry in range(max_retries):
                print(audio_url)
                audio_response = requests.get(audio_url)
                print(audio_response.status_code)
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
                    break
                elif response.status_code == 404:
                    print('404 here')
                time.sleep(2)

        else:
            print(response.json())
#         time.sleep(3)
    # Kết hợp (merge) các audio trong danh sách
    merged_audio = concatenate_audioclips(audio_clips)
    # Lưu âm thanh kết hợp thành tệp mới
    merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
    merged_audio = AudioFileClip("merged_audio.mp3")
    audio_duration = merged_audio.duration
    new_video = video_clip.set_duration(audio_duration)
    video_with_new_audio = new_video.set_audio(merged_audio)
    video_with_new_audio.write_videofile(final_video, codec='libx264', audio_codec='aac')
    os.remove(output_audio_file)

    return '/media/Files/previews/output.mp4'

def is_valid_time_format(time_str):
    # Định dạng thời gian "HH:MM:SS,sss --> HH:MM:SS,sss" (giờ, phút, giây, mili-giây)
    time_format = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
    return bool(re.match(time_format, time_str))

def add_voice_tool(request, id, subtitle_id):
    upload = Upload.objects.get(id=id)
    subtitle = Subtitle.objects.get(id=subtitle_id)
    if subtitle.path.path is not None:
        subtitles = detect_subtitle(subtitle.path.path)
    data = {
        'id':id,
        'video_url': upload.path_video.url,
        'full_path': upload.path_video.path,
        'subtitles': subtitles
    }
    return render(request, "clients/add_voice_tool.html", data)

def merge_video(request):
    context = base_context(request)
    if request.method == 'POST' and 'video_files' in request.FILES:
        if request.session.get('user_id') is None:
            return redirect('users:signin')
        video_files = request.FILES.getlist('video_files')
        for video_file in video_files:
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

def merge_tools(request, id):
    upload = Upload.objects.get(id=id)
    video_list = Upload.objects.filter(userupload__user_id=request.session.get('user_id'))
    return render(request, "clients/merge_tools.html", {'id': id, 'video_url': upload.path_video.url, 'full_path': upload.path_video.path, 'video_list': video_list})

def preview_merge_video(request):
    if request.method == 'POST':
        video_ids = request.POST.get('video_ids')
        video_ids = json.loads(video_ids)
        video_clips = []
        for video_id in video_ids:
            upload = Upload.objects.get(id=video_id)
            video_path = upload.path_video.path
            video_clip = VideoFileClip(video_path)
            video_clips.append(video_clip)
        merged_video = concatenate_videoclips(video_clips)
        merged_video_path = f'media/Files/previews/merged_video_output.mp4'
        merged_video.write_videofile(merged_video_path)
        preview_video = f'/{merged_video_path}'
        return JsonResponse({'preview_video': preview_video})
    
def export_merge_video(request):
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

def crop_video(request):
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
        redirect_url = reverse('clients:crop_tool', kwargs={'id': upload_id})
        return redirect(redirect_url)
    else:
        return render(request, 'clients/crop_video.html', context)

def crop_tool(request, id):
    upload = Upload.objects.get(id=id)
    return render(request, "clients/crop_tool.html", {'id':id,'video_url': upload.path_video.url, 'full_path': upload.path_video.path})


def preview_crop_video(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        upload = Upload.objects.get(id=id)
        x = request.POST.get('x')
        y = request.POST.get('y')
        width = request.POST.get('width')
        height = request.POST.get('height')
        input_video_path = request.POST.get('video_path')
        output_video_path = os.path.join(settings.BASE_DIR, f"media/Files/previews/output_preview_{id}.mp4")
        
        command = f'ffmpeg -i {input_video_path} -filter:v crop={width}:{height}:{x}:{y} {output_video_path}'
        subprocess.call(command, shell=True)
        preview_video = f"/media/Files/previews/output_preview_{id}.mp4"
        return JsonResponse({'preview_video' : preview_video})
    content = {
            'id': id,
            'video_url': upload.path_video.url,
            'full_path': upload.path_video.path
        }
    return render(request, "clients/crop_tool.html", content)

def export_crop_video(request):
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

def export_video(request):
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