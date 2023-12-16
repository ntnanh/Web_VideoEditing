from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'clients/index.html')

def all_tools(request):
    return render(request, 'clients/all_tools.html')



# def clients(request):
#     return render(request, 'clients/index.html')

