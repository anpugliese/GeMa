from django.urls import path

from . import views

app_name = 'gema'
urlpatterns = [
    path('', views.index, name='index'),
     path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path("geoids", views.geoids, name='geoids'),
    path("orthometric-height", views.get_orthometric_height, name='h'),
]