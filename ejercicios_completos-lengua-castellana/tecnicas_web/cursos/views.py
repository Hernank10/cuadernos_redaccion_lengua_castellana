from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Curso, Leccion, Inscripcion
from core.models import Tecnica

@staff_member_required
def crear_curso(request):
    """Vista para crear cursos (solo administradores y profesores)"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        nivel = request.POST.get('nivel')
        duracion_horas = request.POST.get('duracion_horas', 0)
        publicado = request.POST.get('publicado') == 'on'
        tecnicas_ids = request.POST.getlist('tecnicas')
        
        if not titulo or not descripcion:
            messages.error(request, 'Título y descripción son obligatorios')
            return render(request, 'cursos/crear_curso.html', {
                'tecnicas': Tecnica.objects.all()
            })
        
        # Crear curso
        curso = Curso.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            nivel=nivel,
            duracion_horas=duracion_horas,
            publicado=publicado,
            creador=request.user
        )
        
        # Asignar técnicas
        if tecnicas_ids:
            curso.tecnicas.set(tecnicas_ids)
        
        messages.success(request, f'✅ Curso "{curso.titulo}" creado exitosamente')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    # GET - Mostrar formulario
    tecnicas = Tecnica.objects.all()
    context = {
        'tecnicas': tecnicas,
        'titulo': 'Crear Nuevo Curso'
    }
    return render(request, 'cursos/crear_curso.html', context)

@staff_member_required
def editar_curso(request, curso_id):
    """Vista para editar cursos"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Verificar permisos
    if not (request.user.is_superuser or request.user == curso.creador):
        messages.error(request, 'No tienes permisos para editar este curso')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    if request.method == 'POST':
        curso.titulo = request.POST.get('titulo', curso.titulo)
        curso.descripcion = request.POST.get('descripcion', curso.descripcion)
        curso.nivel = request.POST.get('nivel', curso.nivel)
        curso.duracion_horas = request.POST.get('duracion_horas', curso.duracion_horas)
        curso.publicado = request.POST.get('publicado') == 'on'
        curso.save()
        
        # Actualizar técnicas
        tecnicas_ids = request.POST.getlist('tecnicas')
        curso.tecnicas.set(tecnicas_ids)
        
        messages.success(request, f'✅ Curso "{curso.titulo}" actualizado')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    context = {
        'curso': curso,
        'tecnicas': Tecnica.objects.all(),
        'titulo': f'Editar: {curso.titulo}'
    }
    return render(request, 'cursos/crear_curso.html', context)

@staff_member_required
def eliminar_curso(request, curso_id):
    """Eliminar un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if not (request.user.is_superuser or request.user == curso.creador):
        messages.error(request, 'No tienes permisos para eliminar este curso')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    if request.method == 'POST':
        titulo = curso.titulo
        curso.delete()
        messages.success(request, f'✅ Curso "{titulo}" eliminado')
        return redirect('cursos:lista')
    
    context = {
        'curso': curso,
        'titulo': f'Eliminar: {curso.titulo}'
    }
    return render(request, 'cursos/eliminar_curso.html', context)

@staff_member_required
def agregar_leccion(request, curso_id):
    """Agregar una lección a un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if not (request.user.is_superuser or request.user == curso.creador):
        messages.error(request, 'No tienes permisos para agregar lecciones')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        tecnica_id = request.POST.get('tecnica')
        duracion_minutos = request.POST.get('duracion_minutos', 5)
        orden = request.POST.get('orden', curso.lecciones.count() + 1)
        
        if not titulo:
            messages.error(request, 'El título es obligatorio')
            return render(request, 'cursos/agregar_leccion.html', {'curso': curso})
        
        tecnica = None
        if tecnica_id:
            tecnica = get_object_or_404(Tecnica, id=tecnica_id)
        
        leccion = Leccion.objects.create(
            curso=curso,
            titulo=titulo,
            descripcion=descripcion,
            tecnica=tecnica,
            orden=orden,
            duracion_minutos=duracion_minutos
        )
        
        messages.success(request, f'✅ Lección "{leccion.titulo}" agregada')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    context = {
        'curso': curso,
        'tecnicas': Tecnica.objects.all(),
        'titulo': f'Agregar Lección a {curso.titulo}'
    }
    return render(request, 'cursos/agregar_leccion.html', context)
