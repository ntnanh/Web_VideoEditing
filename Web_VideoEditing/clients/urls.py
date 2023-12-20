from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('all_tools', views.all_tools, name="all_tools"),
    path('add_subtitles', views.add_subtitles, name="add_subtitles"),

]