from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProgresoLeccion, Inscripcion, PuntosUsuario, ActividadUsuario, Insignia, InsigniaUsuario

@receiver(post_save, sender=ProgresoLeccion)
def actualizar_gamificacion_leccion(sender, instance, **kwargs):
    if instance.completado and not getattr(instance, '_gamificacion_procesada', False):
        instance._gamificacion_procesada = True
        puntos, _ = PuntosUsuario.objects.get_or_create(usuario=instance.estudiante)
        puntos.total_puntos += 10
        puntos.save()
        
        ActividadUsuario.objects.create(
            usuario=instance.estudiante,
            tipo='leccion_completada',
            descripcion=f"Completó: {instance.leccion.titulo}",
            puntos=10
        )
        
        # Verificar insignias
        total_puntos = puntos.total_puntos
        insignias_disponibles = Insignia.objects.filter(puntos_requeridos__lte=total_puntos)
        for insignia in insignias_disponibles:
            InsigniaUsuario.objects.get_or_create(
                usuario=instance.estudiante,
                insignia=insignia
            )

@receiver(post_save, sender=Inscripcion)
def actualizar_gamificacion_curso(sender, instance, **kwargs):
    if instance.estado == 'completado' and not getattr(instance, '_gamificacion_procesada', False):
        instance._gamificacion_procesada = True
        puntos, _ = PuntosUsuario.objects.get_or_create(usuario=instance.estudiante)
        puntos.total_puntos += 100
        puntos.save()
        
        ActividadUsuario.objects.create(
            usuario=instance.estudiante,
            tipo='curso_completado',
            descripcion=f"Completó el curso: {instance.curso.titulo}",
            puntos=100
        )
