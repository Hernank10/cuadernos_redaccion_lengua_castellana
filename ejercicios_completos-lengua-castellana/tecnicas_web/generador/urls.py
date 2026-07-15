from django.urls import path
from . import views

app_name = 'generador'

urlpatterns = [
    path('', views.dashboard_generador, name='dashboard'),
    path('generar/', views.generar_evaluacion, name='generar'),
]
