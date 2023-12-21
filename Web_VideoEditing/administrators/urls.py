from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index_admin, name="index_admin"),
    path('detail_user', views.detail_user, name="detail_user"),
    
]
