from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from .models import Certificado, Inscripcion

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
    
    if certificado.pdf_file:
        response = HttpResponse(certificado.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificado_{certificado.usuario.username}_{certificado.curso.id}.pdf"'
        return response
    
    messages.error(request, 'No se pudo generar el certificado')
    return redirect('cursos:mis_certificados')

@login_required
def verificar_certificado(request, codigo):
    """Verifica la validez de un certificado por código"""
    certificado = get_object_or_404(Certificado, codigo=codigo)
    
    context = {
        'certificado': certificado,
        'valido': True,
        'titulo': 'Verificar Certificado'
    }
    return render(request, 'cursos/verificar_certificado.html', context)
