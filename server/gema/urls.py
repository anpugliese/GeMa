from django.urls import path

from . import views

app_name = 'gema'
urlpatterns = [
    path("geoids", views.geoids, name='geoids'),
    path("orthometric-height", views.get_orthometric_height, name='h'),
]