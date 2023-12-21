from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'clients/index.html')

def all_tools(request):
    return render(request, 'clients/all_tools.html')

def add_subtitles(request):
    return render(request, 'clients/add_subtitles.html')

def cut_video(request):
    return render(request, 'clients/cut_video.html')
def cut_tool(request):
    return render(request, 'clients/cut_tool.html')

def loop_video(request):
    return render(request, 'clients/loop_video.html')

def loop_tool(request):
    return render(request, 'clients/loop_tool.html')

# def clients(request):
#     return render(request, 'clients/index.html')

