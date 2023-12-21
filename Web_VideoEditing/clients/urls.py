from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('all_tools', views.all_tools, name="all_tools"),
    path('add_subtitles', views.add_subtitles, name="add_subtitles"),
    path('merge_video', views.merge_video, name="merge_video"),
    path('merge_tools', views.merge_tools, name="merge_tools"),
    path('crop_video', views.crop_video, name="crop_video"),
    path('crop_tools', views.crop_tools, name="crop_tools"),
]