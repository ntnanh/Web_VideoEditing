from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from users.views import base_context
from users.models import Users
from clients.models import Video
from .forms import UserForm
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError




def check_user_role(request):
    if 'username' not in request.session:
        return redirect('users:signin')
    
    username = request.session.get('username', None)
    user_profile = Users.objects.get(username=username) if username else None
    
    if user_profile.role == 'client':
        return redirect('user_project:index',id=user_profile.id)
    
    return None

def detail_user(request):
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    
    context = base_context(request)
    return render(request, 'administrators/detail_user.html', context)

def index(request):
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    
    context = base_context(request)
    return render(request, 'administrators/index.html', context)

def table(request):
    redirect_result = check_user_role(request)
    if redirect_result:
        return redirect_result
    users_data = Users.objects.all()
    context = base_context(request)
    user_profile = context['user_profile']
    return render(request, 'administrators/table.html',{'users_data': users_data, 'user_profile': user_profile})


def delete_user(request, user_id):
    try:
        user = Users.objects.get(id=user_id)
        user.delete()
    except Users.DoesNotExist:
        pass
    return redirect('administrators:table') 

def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        image = request.FILES.get('image', 'default.jpg')
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
        mysqluser = Users(username=username, email=email, password=hashed_password, role=role, image=image)
        # dd(mysqluser)
        mysqluser.save()
    
        return redirect('administrators:table') 
    
    context = base_context(request)
    user_profile = context['user_profile']
    return render(request,'administrators/add_user.html',{'user_profile':user_profile})

def update_user(request, user_id):
    user = Users.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('administrators:table')
    else:
        form = UserForm(instance=user)
    
    context = base_context(request)
    user_profile = context['user_profile']

    return render(request, 'administrators/update_user.html', {'form': form, 'user': user, 'user_profile':user_profile})

# def video_user(request):
#     context = base_context(request)
#     user_profile = context['user_profile']
#     return render(request,'administrators/video_user.html',{'user_profile':user_profile})

# def video_user(request):
     # Assuming you have a user profile model and the user is authenticated
    # context = base_context(request)
    # user_profile = context['user_profile']
    # user = Users.objects.get(id=user_id)  # Assuming you have a User model
    
    # videos = Video.objects.filter(user=user)
    
    # context1 = {
    #     'user_profile': user_profile,
    #     'user': user,
    #     'videos': videos,
    # }
    
    # return render(request, 'administrators/video_user.html', {'user_profile':user_profile})
# administrators/views.py

# def video_user(request, pk):
#     videos = Video.objects.filter(user_id=pk)
#     return render(request, 'administrators/video_user.html', {'videos': videos, 'user_id': pk})
def video_user(request, pk):
    # Lấy dữ liệu video của người dùng với id tương ứng
    videos = Video.objects.filter(user_id=pk)
    return render(request, 'video_user.html', {'videos': videos})