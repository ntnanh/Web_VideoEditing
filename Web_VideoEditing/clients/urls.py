from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('all_tools', views.all_tools, name="all_tools"),
    path('add_subtitles', views.add_subtitles, name="add_subtitles"),
    path('merge_video', views.merge_video, name="merge_video"),
    path('merge_tools', views.merge_tools, name="merge_tools"),
    path('crop_video', views.crop_video, name="crop_video"),
<<<<<<< HEAD
    path('crop_tools', views.crop_tools, name="crop_tools"),
=======
    path('crop_tool', views.crop_tool, name="crop_tool"),
>>>>>>> cf57c1ca94a4aad4efaed6df5e757b9f6b2b195b
    path('cut_tool', views.cut_tool, name="cut_tool"),
    path('cut_video', views.cut_video, name="cut_video"),
    path('loop_video', views.loop_video, name="loop_video"),
    path('loop_tool', views.loop_tool, name="loop_tool"),

]