from django.urls import path, include
from .import views

app_name = 'clients'
urlpatterns = [
    path('', views.home, name="home"),
    path('all_tools/', views.all_tools, name="all_tools"),
    path('add_subtitles/', views.subtitle_video, name="add_subtitles"),
    path('add_subtitles_tool/<int:id>/<int:subtitle_id>/', views.add_subtitles_tool, name="add_subtitles_tool"),
    path('preview_add_subtitles', views.preview_add_subtitles, name="preview_add_subtitles"),
    path('subtitle/<int:id>/', views.subtitle, name="subtitle"),
    path('merge_video/', views.merge_video, name="merge_video"),
    path('preview_merge_video/', views.preview_merge_video, name='preview_merge_video'),
    path('merge_tools/<int:id>/', views.merge_tools, name="merge_tools"),
    path('export_merge_video', views.export_merge_video, name="export_merge_video"),
    path('crop_video/', views.crop_video, name="crop_video"),
    path('crop_tool/<int:id>/', views.crop_tool, name="crop_tool"),
    path('preview_crop_video', views.preview_crop_video, name="preview_crop_video"),
    path('export_crop_video', views.export_crop_video, name="export_crop_video"),
    path('cut_tool/<int:id>/', views.cut_tool, name="cut_tool"),
    path('cut_video/', views.cut_video, name="cut_video"),
    path('loop_video/', views.loop_video, name="loop_video"),
    path('loop_tool/<int:id>/', views.loop_tool, name="loop_tool"),
    path('export_loop_video', views.export_loop_video, name="export_loop_video"),
    path('preview_cut_video', views.preview_cut_video, name="preview_cut_video"),
    path('export_video', views.export_video, name="export_video"),
    path('add_voice_tool/<int:id>/<int:subtitle_id>/', views.add_voice_tool, name="add_voice_tool"),
    path('add_voice/', views.add_voice, name="add_voice"),
    path('subtitle_voice/<int:id>/', views.subtitle_voice, name="subtitle_voice"),
    path('upload_subtitle', views.upload_subtitle, name="upload_subtitle"),
    path('preview_voice_to_video', views.preview_voice_to_video, name="preview_voice_to_video"),


]