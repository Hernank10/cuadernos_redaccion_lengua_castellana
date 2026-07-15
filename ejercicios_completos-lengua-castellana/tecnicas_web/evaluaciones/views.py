from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Evaluacion, Pregunta, RespuestaUsuario, ResultadoEvaluacion
import json

@login_required
def evaluaciones_list(request):
    """Lista de evaluaciones disponibles para estudiantes"""
    evaluaciones = Evaluacion.objects.filter(publicado=True)
    
    # Verificar si el usuario ya completó cada evaluación
    for eval in evaluaciones:
        eval.completada = ResultadoEvaluacion.objects.filter(
            usuario=request.user,
            evaluacion=eval
        ).exists()
    
    context = {
        'evaluaciones': evaluaciones,
        'titulo': 'Evaluaciones Disponibles'
    }
    return render(request, 'evaluaciones/lista.html', context)

@login_required
def evaluacion_detail(request, evaluacion_id):
    """Detalle de una evaluación"""
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, publicado=True)
    preguntas = evaluacion.preguntas.all().order_by('orden')
    
    # Verificar si ya fue completada
    resultado = ResultadoEvaluacion.objects.filter(
        usuario=request.user,
        evaluacion=evaluacion
    ).first()
    
    if resultado:
        # Si ya fue completada, mostrar resultados
        respuestas = RespuestaUsuario.objects.filter(
            usuario=request.user,
            pregunta__evaluacion=evaluacion
        )
        return render(request, 'evaluaciones/resultados.html', {
            'evaluacion': evaluacion,
            'resultado': resultado,
            'respuestas': respuestas,
            'titulo': f'Resultados - {evaluacion.titulo}'
        })
    
    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
        'total_preguntas': preguntas.count(),
        'titulo': evaluacion.titulo
    }
    return render(request, 'evaluaciones/tomar.html', context)

@login_required
def guardar_respuesta(request):
    """Guarda una respuesta del usuario (AJAX)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        pregunta_id = data.get('pregunta_id')
        respuesta = data.get('respuesta')
        
        pregunta = get_object_or_404(Pregunta, id=pregunta_id)
        
        # Guardar respuesta
        respuesta_obj, created = RespuestaUsuario.objects.update_or_create(
            usuario=request.user,
            pregunta=pregunta,
            defaults={'respuesta': str(respuesta)}
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)

@login_required
def finalizar_evaluacion(request, evaluacion_id):
    """Finaliza una evaluación y calcula el resultado"""
    if request.method == 'POST':
        evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
        preguntas = evaluacion.preguntas.all()
        
        # Obtener todas las respuestas del usuario
        respuestas = RespuestaUsuario.objects.filter(
            usuario=request.user,
            pregunta__evaluacion=evaluacion
        )
        
        # Calcular puntaje
        puntaje_total = 0
        preguntas_correctas = 0
        
        for pregunta in preguntas:
            respuesta = respuestas.filter(pregunta=pregunta).first()
            if respuesta:
                # Evaluar según el tipo de pregunta
                if pregunta.tipo == 'multiple':
                    if str(respuesta.respuesta) == str(pregunta.respuesta_correcta):
                        puntaje_total += pregunta.puntaje
                        preguntas_correctas += 1
                elif pregunta.tipo == 'verdadero_falso':
                    if str(respuesta.respuesta).upper() == pregunta.respuesta_correcta.upper():
                        puntaje_total += pregunta.puntaje
                        preguntas_correctas += 1
                elif pregunta.tipo == 'completar':
                    if str(respuesta.respuesta).lower().strip() == str(pregunta.respuesta_correcta).lower().strip():
                        puntaje_total += pregunta.puntaje
                        preguntas_correctas += 1
                # Para preguntas abiertas, se califica manualmente
        
        # Calcular porcentaje
        total_posible = sum(p.puntaje for p in preguntas)
        porcentaje = (puntaje_total / total_posible) * 100 if total_posible > 0 else 0
        
        # Guardar resultado
        resultado = ResultadoEvaluacion.objects.create(
            usuario=request.user,
            evaluacion=evaluacion,
            puntaje_obtenido=porcentaje,
            aprobado=porcentaje >= 60,  # 60% para aprobar
            fecha_completado=timezone.now()
        )
        
        messages.success(request, f'✅ Evaluación completada! Puntaje: {porcentaje:.1f}%')
        return redirect('evaluaciones:resultados', evaluacion_id=evaluacion_id)
    
    return redirect('evaluaciones:detalle', evaluacion_id=evaluacion_id)

@login_required
def resultados(request, evaluacion_id):
    """Muestra los resultados de una evaluación"""
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
    resultado = get_object_or_404(ResultadoEvaluacion, 
                                   usuario=request.user, 
                                   evaluacion=evaluacion)
    
    respuestas = RespuestaUsuario.objects.filter(
        usuario=request.user,
        pregunta__evaluacion=evaluacion
    )
    
    # Preparar datos para mostrar
    preguntas_data = []
    for pregunta in evaluacion.preguntas.all().order_by('orden'):
        respuesta = respuestas.filter(pregunta=pregunta).first()
        es_correcta = False
        if respuesta:
            if pregunta.tipo == 'multiple':
                es_correcta = str(respuesta.respuesta) == str(pregunta.respuesta_correcta)
            elif pregunta.tipo == 'verdadero_falso':
                es_correcta = str(respuesta.respuesta).upper() == pregunta.respuesta_correcta.upper()
            elif pregunta.tipo == 'completar':
                es_correcta = str(respuesta.respuesta).lower().strip() == str(pregunta.respuesta_correcta).lower().strip()
        
        preguntas_data.append({
            'pregunta': pregunta,
            'respuesta_usuario': respuesta.respuesta if respuesta else 'No respondida',
            'respuesta_correcta': pregunta.respuesta_correcta,
            'es_correcta': es_correcta,
            'puntaje_obtenido': pregunta.puntaje if es_correcta else 0,
            'tipo': pregunta.tipo
        })
    
    context = {
        'evaluacion': evaluacion,
        'resultado': resultado,
        'preguntas_data': preguntas_data,
        'titulo': f'Resultados - {evaluacion.titulo}'
    }
    return render(request, 'evaluaciones/resultados.html', context)
