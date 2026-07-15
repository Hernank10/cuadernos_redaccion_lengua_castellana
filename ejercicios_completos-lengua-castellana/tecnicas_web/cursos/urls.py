from django.urls import path
from . import views
from . import views_lms
from . import views_gamificacion

app_name = 'cursos'

urlpatterns = [
    # Vistas públicas
    path('', views_lms.cursos_list, name='lista'),
    path('<int:curso_id>/', views_lms.curso_detail, name='detalle'),
    path('<int:curso_id>/leccion/<int:leccion_id>/', views_lms.leccion_detail, name='leccion_detalle'),
    path('<int:curso_id>/leccion/<int:leccion_id>/completar/', views_lms.completar_leccion, name='completar'),
    
    # Vistas de administración
    path('crear/', views.crear_curso, name='crear'),
    path('<int:curso_id>/editar/', views.editar_curso, name='editar'),
    path('<int:curso_id>/eliminar/', views.eliminar_curso, name='eliminar'),
    path('<int:curso_id>/leccion/agregar/', views.agregar_leccion, name='agregar_leccion'),
    
    # Gamificación
    path('gamificacion/', views_gamificacion.gamificacion, name='gamificacion'),
    path('ranking/', views_gamificacion.ranking, name='ranking'),
]
