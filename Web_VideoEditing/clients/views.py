from django.shortcuts import render
from django.http import HttpResponse
def clients(request):
    return render(request, 'clients/index.html')



# def clients2(request):
#     return HttpResponse('hello world 111')
# def all_tools(request):
#     return render(request, 'clients/all_tools.html')
# def index(request):
#     return render(request, 'clients/index.html')
