from django.urls import path
from . import views

app_name = 'evaluaciones'

urlpatterns = [
    path('', views.evaluaciones_list, name='lista'),
    path('<int:evaluacion_id>/', views.evaluacion_detail, name='detalle'),
    path('<int:evaluacion_id>/tomar/', views.evaluacion_detail, name='tomar'),
    path('<int:evaluacion_id>/resultados/', views.resultados, name='resultados'),
    path('<int:evaluacion_id>/finalizar/', views.finalizar_evaluacion, name='finalizar'),
    path('guardar-respuesta/', views.guardar_respuesta, name='guardar_respuesta'),
]
