from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Curso, Leccion, Inscripcion, ProgresoLeccion

def cursos_list(request):
    """Lista de cursos disponibles"""
    cursos = Curso.objects.filter(publicado=True)
    
    # Estadísticas por curso
    for curso in cursos:
        curso.total_lecciones = curso.lecciones.count()
        curso.estudiantes_count = curso.get_estudiantes_count()
    
    context = {
        'cursos': cursos,
        'titulo': 'Cursos Disponibles'
    }
    return render(request, 'cursos/lista.html', context)

@login_required
def curso_detail(request, curso_id):
    """Detalle de un curso con lecciones"""
    curso = get_object_or_404(Curso, id=curso_id, publicado=True)
    lecciones = curso.lecciones.all().order_by('orden')
    
    # Verificar si el usuario está inscrito
    inscrito = Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists()
    
    # Progreso del usuario
    progreso = {}
    if inscrito:
        for leccion in lecciones:
            prog, created = ProgresoLeccion.objects.get_or_create(
                estudiante=request.user,
                leccion=leccion
            )
            progreso[leccion.id] = prog.completado
    
    # Calcular progreso total
    total_lecciones = lecciones.count()
    completadas = sum(1 for p in progreso.values() if p)
    progreso_total = int((completadas / total_lecciones) * 100) if total_lecciones > 0 else 0
    
    context = {
        'curso': curso,
        'lecciones': lecciones,
        'inscrito': inscrito,
        'progreso': progreso,
        'progreso_total': progreso_total,
        'titulo': curso.titulo
    }
    return render(request, 'cursos/detalle.html', context)

@login_required
def leccion_detail(request, curso_id, leccion_id):
    """Detalle de una lección (técnica individual)"""
    curso = get_object_or_404(Curso, id=curso_id)
    leccion = get_object_or_404(Leccion, id=leccion_id, curso=curso)
    
    # Registrar progreso
    progreso, created = ProgresoLeccion.objects.get_or_create(
        estudiante=request.user,
        leccion=leccion
    )
    
    # Obtener técnica asociada
    tecnica = leccion.tecnica
    
    # Obtener siguiente y anterior lección
    anterior = Leccion.objects.filter(curso=curso, orden__lt=leccion.orden).order_by('-orden').first()
    siguiente = Leccion.objects.filter(curso=curso, orden__gt=leccion.orden).order_by('orden').first()
    
    context = {
        'curso': curso,
        'leccion': leccion,
        'tecnica': tecnica,
        'progreso': progreso,
        'anterior': anterior,
        'siguiente': siguiente,
        'titulo': f"{curso.titulo} - {leccion.titulo}"
    }
    return render(request, 'cursos/leccion.html', context)

@login_required
def completar_leccion(request, curso_id, leccion_id):
    """Marcar una lección como completada"""
    if request.method == 'POST':
        curso = get_object_or_404(Curso, id=curso_id)
        leccion = get_object_or_404(Leccion, id=leccion_id, curso=curso)
        
        progreso, created = ProgresoLeccion.objects.get_or_create(
            estudiante=request.user,
            leccion=leccion
        )
        progreso.completado = True
        progreso.save()
        
        messages.success(request, f'¡Completaste la lección: {leccion.titulo}!')
        
        # Verificar si el curso está completo
        lecciones_curso = curso.lecciones.count()
        completadas = ProgresoLeccion.objects.filter(
            estudiante=request.user,
            leccion__curso=curso,
            completado=True
        ).count()
        
        if completadas == lecciones_curso:
            # Actualizar inscripción a completado
            inscripcion = Inscripcion.objects.filter(
                estudiante=request.user,
                curso=curso
            ).first()
            if inscripcion:
                inscripcion.estado = 'completado'
                inscripcion.progreso = 100
                inscripcion.save()
            messages.success(request, f'🎉 ¡Felicidades! Completaste el curso: {curso.titulo}')
    
    return redirect('cursos:detalle', curso_id=curso_id)
