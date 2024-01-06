from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'administrators'
urlpatterns = [
    path('', views.index, name="index"),
    path('detail_user', views.detail_user, name="detail_user"),
    # path('index', views.index, name="index"),
    path('table', views.table, name="table"),
    path('add_user', views.add_user, name="add_user"),
    path('video_user/<int:pk>/', views.video_user, name='video_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),

]
