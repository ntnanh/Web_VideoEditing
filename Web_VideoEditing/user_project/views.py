from django.shortcuts import render, redirect
from users.models import Users
from clients.models import Upload, UserUpload
from django.http import HttpResponse
from django.urls import reverse
from users.views import base_context
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import os
from django.http import FileResponse
from django.utils.encoding import smart_str


def check_user_role(request):
    if 'username' not in request.session:
        return redirect('users:signin')
    username = request.session.get('username', None)
    user_profile = Users.objects.get(username=username) if username else None
    if user_profile.role == 'admin':
        return redirect('administrators:index')
    return None

def home(request, id):
    user = Users.objects.get(pk=id)
    user_uploads = UserUpload.objects.filter(user=user)
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    context = base_context(request)
    user_profile = context['user_profile']
    return render(request, 'user_project/index.html', {'user': user, 'user_uploads': user_uploads, 'user_profile': user_profile})

def forgot_password(request):
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    context = base_context(request)
    user_profile = context['user_profile']
    return render(request, 'user_project/forgot_password.html',{'user_profile': user_profile})

# def profile(request,user_id):
#     user_profile1 = Users.objects.get(id=user_id)
#     context = base_context(request)
#     user_profile = context['user_profile']
#     return render(request, 'user_project/profile.html', {'user_profile1':user_profile1,'user_profile':user_profile})

def profile(request, user_id):
    user_profile1 = get_object_or_404(Users, id=user_id)
    context = base_context(request)
    user_profile = context['user_profile']

    if request.method == 'POST':
        # Retrieve the submitted form data
        new_name = request.POST.get('editName')
        new_email = request.POST.get('editEmail')
        new_image = request.FILES.get('image')

        # Update the user profile
        user_profile1.username = new_name
        user_profile1.email = new_email

        # Save the uploaded image if provided
        if new_image:
            user_profile1.image = new_image

        user_profile1.save()

    return render(request, 'user_project/profile.html', {'user_profile1': user_profile1, 'user_profile': user_profile})


def delete_video(request, pk):
    user_upload = get_object_or_404(UserUpload, pk=pk)
    user_upload.delete()
    return redirect('user_project:index', id=user_upload.user.id)

def edit_user(request):
    pass

# def download_video(request, pk):
#     user_upload = get_object_or_404(UserUpload, pk=pk)
#     user_upload.delete()
#     return redirect('user_project:index', id=user_upload.user.id)

def download_video(request, pk):
    upload = get_object_or_404(Upload, pk=pk)

    # Get the path of the video file
    video_path = upload.path_video.path

    # Open the video file
    video_file = open(video_path, 'rb')

    # Create a FileResponse with the video file
    response = FileResponse(video_file)

    # Set the content type and headers for the response
    response['Content-Type'] = 'video/mp4'
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(upload.path_video.name)

    return response



def edited_video(request):
    return render(request, 'user_project/edited_video.html')