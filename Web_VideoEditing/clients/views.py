from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def clients(request):
    return render(request, 'clients/index.html')
# def clients2(request):
#     return HttpResponse('hello world 111')