from django.shortcuts import render
from users.views import base_context

# Create your views here.
# def index_admin(request):
#     return render(request, 'administrators/index_admin.html')

def detail_user(request):
    context = base_context(request)
    return render(request, 'administrators/detail_user.html',context)

def index(request):
    context = base_context(request)
    return render(request, 'administrators/index.html',context)

def table(request):
    context = base_context(request)
    return render(request, 'administrators/table.html',context)