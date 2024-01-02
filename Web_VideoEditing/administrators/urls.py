from django.urls import path, include
from . import views
app_name = 'administrators'
urlpatterns = [
    path('', views.index, name="index"),
    path('detail_user', views.detail_user, name="detail_user"),
    # path('index', views.index, name="index"),
    path('table', views.table, name="table"),



]
