from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from .models import Certificado, Inscripcion, Curso

@login_required
def mis_certificados(request):
    """Vista para listar los certificados del usuario"""
    certificados = Certificado.objects.filter(usuario=request.user).order_by('-fecha_emision')
    
    context = {
        'certificados': certificados,
        'titulo': 'Mis Certificados'
    }
    return render(request, 'cursos/mis_certificados.html', context)

@login_required
def ver_certificado(request, certificado_id):
    """Vista para ver un certificado específico"""
    certificado = get_object_or_404(Certificado, id=certificado_id, usuario=request.user)
    
    context = {
        'certificado': certificado,
        'titulo': f'Certificado - {certificado.curso.titulo}'
    }
    return render(request, 'cursos/ver_certificado.html', context)

@login_required
def descargar_certificado(request, certificado_id):
    """Descarga el PDF del certificado"""
    certificado = get_object_or_404(Certificado, id=certificado_id, usuario=request.user)
    
    if not certificado.pdf_file:
        messages.error(request, 'El certificado aún no tiene PDF generado')
        return redirect('cursos:mis_certificados')
    
    response = HttpResponse(certificado.pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{certificado.usuario.username}_{certificado.curso.id}.pdf"'
    return response

def verificar_certificado(request, codigo):
    """Verifica la validez de un certificado por código (público)"""
    try:
        certificado = Certificado.objects.get(codigo=codigo)
        context = {
            'certificado': certificado,
            'valido': True,
            'titulo': 'Verificar Certificado'
        }
        return render(request, 'cursos/verificar_certificado.html', context)
    except Certificado.DoesNotExist:
        context = {
            'certificado': None,
            'valido': False,
            'titulo': 'Verificar Certificado'
        }
        return render(request, 'cursos/verificar_certificado.html', context)

@login_required
def certificado_curso(request, curso_id):
    """Vista para ver el certificado de un curso específico"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Verificar si el usuario completó el curso
    inscripcion = Inscripcion.objects.filter(
        estudiante=request.user,
        curso=curso,
        estado='completado'
    ).first()
    
    if not inscripcion:
        messages.error(request, 'Debes completar el curso para obtener el certificado')
        return redirect('cursos:detalle', curso_id=curso.id)
    
    # Buscar certificado
    certificado = Certificado.objects.filter(
        usuario=request.user,
        curso=curso
    ).first()
    
    if not certificado:
        # Crear certificado si no existe
        from django.utils import timezone
        certificado = Certificado.objects.create(
            usuario=request.user,
            curso=curso,
            fecha_completado=timezone.now(),
            puntuacion=inscripcion.calificacion or 0,
            horas=curso.duracion_horas
        )
        messages.success(request, '✅ Certificado generado exitosamente')
    
    context = {
        'certificado': certificado,
        'titulo': f'Certificado - {curso.titulo}'
    }
    return render(request, 'cursos/ver_certificado.html', context)
