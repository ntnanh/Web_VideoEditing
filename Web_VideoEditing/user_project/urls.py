from django.urls import path
from . import views

app_name = 'user_project'
urlpatterns = [
path('', views.home, name='index'),
path('forgot_password/', views.forgot_password, name='forgot_password'),

]
