from django.urls import path
from . import views

app_name = 'evaluaciones'

urlpatterns = [
    path('', views.evaluaciones_list, name='lista'),
    path('<int:evaluacion_id>/', views.evaluacion_detail, name='detalle'),
]
