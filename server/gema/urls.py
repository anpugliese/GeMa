from django.urls import path

from . import views

app_name = 'gema'
urlpatterns = [
    path("geoids", views.geoids, name='geoids'),
    path("geoids-list", views.geoids_list, name='geoids_list'),
    path("orthometric-height", views.get_orthometric_height, name='h'),
    path("orthometric-height-list", views.get_orthometric_height_list, name='h_list'),
]