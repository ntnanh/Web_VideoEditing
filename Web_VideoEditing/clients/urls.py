from django.urls import path
from .import views

urlpatterns = [
    path('', views.clients)
    # path('2/', views.clients2)
]




# urlpatterns = [
#     path('index/', views.clients, name='index'),
#     path('all_tools/', views.clients, name='all_tools'),

# ]
