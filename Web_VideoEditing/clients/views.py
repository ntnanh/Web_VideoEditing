from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'clients/index.html')

def all_tools(request):
    return render(request, 'clients/all_tools.html')

def add_subtitles(request):
    return render(request, 'clients/add_subtitles.html')

<<<<<<< HEAD
def merge_video(request):
    return render(request, 'clients/merge_video.html')

def merge_tools(request):
    return render(request, 'clients/merge_tools.html')

def crop_video(request):
    return render(request, 'clients/crop_video.html')

def crop_tools(request):
    return render(request, 'clients/crop_tools.html')

=======
def cut_video(request):
    return render(request, 'clients/cut_video.html')
def cut_tool(request):
    return render(request, 'clients/cut_tool.html')

def loop_video(request):
    return render(request, 'clients/loop_video.html')

def loop_tool(request):
    return render(request, 'clients/loop_tool.html')
>>>>>>> cde8e9d14b0e011e4f044797764594c817295970

# def clients(request):
#     return render(request, 'clients/index.html')

