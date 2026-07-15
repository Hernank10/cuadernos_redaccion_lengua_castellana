from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('tecnicas/', views.tecnicas_list, name='tecnicas_list'),
    path('tecnica/<int:pk>/', views.tecnica_detail, name='tecnica_detail'),
    path('categorias/', views.categorias, name='categorias'),
    path('buscar/', views.buscar, name='buscar'),
]
