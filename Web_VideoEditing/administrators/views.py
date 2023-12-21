from django.shortcuts import render

# Create your views here.
def index_admin(request):
    return render(request, 'administrators/index_admin.html')

def detail_user(request):
    return render(request, 'administrators/detail_user.html')