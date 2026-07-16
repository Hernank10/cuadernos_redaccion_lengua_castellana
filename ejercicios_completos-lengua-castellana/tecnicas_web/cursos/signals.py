from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Inscripcion, Certificado

@receiver(post_save, sender=Inscripcion)
def generar_certificado_al_completar(sender, instance, **kwargs):
    """Genera automáticamente un certificado cuando se completa un curso"""
    
    # Solo generar si el curso está completado y no tiene certificado
    if instance.estado == 'completado':
        # Verificar si ya existe certificado
        certificado_existente = Certificado.objects.filter(
            usuario=instance.estudiante,
            curso=instance.curso
        ).first()
        
        if not certificado_existente:
            # Crear nuevo certificado
            certificado = Certificado.objects.create(
                usuario=instance.estudiante,
                curso=instance.curso,
                fecha_completado=instance.fecha_completado or timezone.now(),
                puntuacion=instance.calificacion,
                horas=instance.curso.duracion_horas
            )
            print(f"✅ Certificado creado para {instance.estudiante.username} - {instance.curso.titulo}")
            
            # Intentar generar PDF (sin el generador para simplificar)
            try:
                # Marcar como generado (simplificado)
                certificado.save()
                print(f"✅ Certificado guardado: {certificado.codigo}")
            except Exception as e:
                print(f"❌ Error guardando certificado: {e}")
