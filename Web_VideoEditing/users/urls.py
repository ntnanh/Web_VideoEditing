from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('postSignup', views.postSignup, name="postSignup"),
    path('postSignin', views.postSignin, name="postSignin"),
    path('signout', views.signout, name="signout"),
]
