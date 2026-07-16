from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Curso, Leccion, Inscripcion, ProgresoLeccion

def cursos_list(request):
    cursos = Curso.objects.filter(publicado=True)
    
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
    completadas = sum(1 for p in progreso.values() if p) if inscrito else 0
    progreso_total = int((completadas / total_lecciones) * 100) if total_lecciones > 0 else 0
    
    # Manejar inscripción (POST)
    if request.method == 'POST' and 'inscribirse' in request.POST:
        if not inscrito:
            Inscripcion.objects.create(
                estudiante=request.user,
                curso=curso,
                estado='activo',
                progreso=0
            )
            messages.success(request, f'✅ Te has inscrito en "{curso.titulo}"')
            return redirect('cursos:detalle', curso_id=curso.id)
    
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
    curso = get_object_or_404(Curso, id=curso_id)
    leccion = get_object_or_404(Leccion, id=leccion_id, curso=curso)
    
    # Verificar inscripción
    inscrito = Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists()
    if not inscrito:
        messages.warning(request, 'Debes inscribirte al curso primero')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    progreso, created = ProgresoLeccion.objects.get_or_create(
        estudiante=request.user,
        leccion=leccion
    )
    
    tecnica = leccion.tecnica
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
    if request.method == 'POST':
        curso = get_object_or_404(Curso, id=curso_id)
        leccion = get_object_or_404(Leccion, id=leccion_id, curso=curso)
        
        # Verificar inscripción
        inscripcion = Inscripcion.objects.filter(estudiante=request.user, curso=curso).first()
        if not inscripcion:
            messages.error(request, 'No estás inscrito en este curso')
            return redirect('cursos:detalle', curso_id=curso.id)
        
        progreso, created = ProgresoLeccion.objects.get_or_create(
            estudiante=request.user,
            leccion=leccion
        )
        progreso.completado = True
        progreso.save()
        
        messages.success(request, f'¡Completaste la lección: {leccion.titulo}!')
        
        # Actualizar progreso del curso
        lecciones_curso = curso.lecciones.count()
        completadas = ProgresoLeccion.objects.filter(
            estudiante=request.user,
            leccion__curso=curso,
            completado=True
        ).count()
        
        progreso_curso = int((completadas / lecciones_curso) * 100) if lecciones_curso > 0 else 0
        inscripcion.progreso = progreso_curso
        
        if completadas == lecciones_curso:
            inscripcion.estado = 'completado'
            inscripcion.fecha_completado = timezone.now()
            messages.success(request, f'🎉 ¡Felicidades! Completaste el curso: {curso.titulo}')
        inscripcion.save()
    
    return redirect('cursos:detalle', curso_id=curso_id)
