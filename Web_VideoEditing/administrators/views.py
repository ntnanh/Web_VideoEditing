from django.shortcuts import render, redirect
from users.views import base_context
from users.models import Users

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
    return render(request, 'administrators/table.html',{'users_data': users_data}, context)