from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evaluacion, ResultadoEvaluacion

@login_required
def evaluaciones_list(request):
    evaluaciones = Evaluacion.objects.filter(publicado=True)
    context = {
        'evaluaciones': evaluaciones,
        'titulo': 'Evaluaciones Disponibles'
    }
    return render(request, 'evaluaciones/lista.html', context)

@login_required
def evaluacion_detail(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, publicado=True)
    preguntas = evaluacion.preguntas.all()
    
    resultado = ResultadoEvaluacion.objects.filter(
        usuario=request.user,
        evaluacion=evaluacion
    ).first()
    
    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
        'resultado': resultado,
        'titulo': evaluacion.titulo
    }
    return render(request, 'evaluaciones/detalle.html', context)
