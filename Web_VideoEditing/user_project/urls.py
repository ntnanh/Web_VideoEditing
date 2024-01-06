from django.urls import path
from . import views

app_name = 'user_project'
urlpatterns = [
path('<int:id>/', views.home, name='index'),
path('forgot_password/', views.forgot_password, name='forgot_password'),
path('profile/<int:user_id>/', views.profile, name='profile'),
path('delete_video/<int:pk>/', views.delete_video, name='delete_video'),
path('edit_user/', views.edit_user, name='edit_user'),
# path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
path('download_video/<int:pk>/', views.download_video, name='download_video'),
path('edited_video/', views.edited_video, name='edited_video'),



]
