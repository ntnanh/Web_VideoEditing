from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('all_tools', views.all_tools, name="all_tools"),
    path('add_subtitles', views.add_subtitles, name="add_subtitles"),
    path('cut_tool', views.cut_tool, name="cut_tool"),
    path('cut_video', views.cut_video, name="cut_video"),
    path('loop_video', views.loop_video, name="loop_video"),
    path('loop_tool', views.loop_tool, name="loop_tool"),

]