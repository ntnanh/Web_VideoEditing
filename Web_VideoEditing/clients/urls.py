from django.urls import path
from .import views

urlpatterns = [
    path('', views.clients)
    # path('2/', views.clients2)

]