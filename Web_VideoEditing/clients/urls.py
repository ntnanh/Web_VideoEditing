from django.urls import path, include
from .import views

# urlpatterns = [
#     path('', views.clients)
#     # path('2/', views.clients2)

# ]

urlpatterns = [
    path('', views.home, name="home"),
    path('all_tools', views.all_tools, name="all_tools"),
]