from django.urls import path, include
from . import views
app_name = 'users'
urlpatterns = [
    # path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
]
