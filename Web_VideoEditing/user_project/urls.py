from django.urls import path
from .import views

app_name = 'user_project'
urlpatterns = [
    path('index', views.home, name="index"),
]