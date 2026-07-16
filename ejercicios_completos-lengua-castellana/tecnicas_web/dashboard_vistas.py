"""
VISTAS PARA DASHBOARD DE ANÁLISIS
"""

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, Sum
from core.models import Tecnica
from usuarios.models import Usuario
from cursos.models import Curso, Inscripcion, ProgresoLeccion, Certificado
from evaluaciones.models import Evaluacion, ResultadoEvaluacion
import json

@staff_member_required
def dashboard_admin(request):
    """Dashboard de administración con estadísticas"""
    
    # Estadísticas básicas
    stats = {
        'usuarios': Usuario.objects.count(),
        'estudiantes': Usuario.objects.filter(rol='estudiante').count(),
        'profesores': Usuario.objects.filter(rol='profesor').count(),
        'tecnicas': Tecnica.objects.count(),
        'cursos': Curso.objects.count(),
        'cursos_publicados': Curso.objects.filter(publicado=True).count(),
        'inscripciones': Inscripcion.objects.count(),
        'inscripciones_activas': Inscripcion.objects.filter(estado='activo').count(),
        'inscripciones_completadas': Inscripcion.objects.filter(estado='completado').count(),
        'evaluaciones': Evaluacion.objects.count(),
        'evaluaciones_publicadas': Evaluacion.objects.filter(publicado=True).count(),
        'resultados': ResultadoEvaluacion.objects.count(),
        'certificados': Certificado.objects.count(),
        'progreso_avg': Inscripcion.objects.aggregate(avg=Avg('progreso'))['avg'] or 0,
    }
    
    # Datos para gráficos
    chart_data = {
        'usuarios_por_rol': list(Usuario.objects.values('rol').annotate(count=Count('id'))),
        'cursos_por_nivel': list(Curso.objects.values('nivel').annotate(count=Count('id'))),
        'evaluaciones_por_tipo': list(Evaluacion.objects.values('tipo').annotate(count=Count('id'))),
        'inscripciones_por_estado': list(Inscripcion.objects.values('estado').annotate(count=Count('id'))),
        'progreso_distribucion': list(Inscripcion.objects.values('progreso').annotate(count=Count('id')).order_by('progreso')[:20]),
    }
    
    context = {
        'stats': stats,
        'chart_data': json.dumps(chart_data),
        'titulo': 'Dashboard de Administración'
    }
    
    return render(request, 'admin/dashboard.html', context)
