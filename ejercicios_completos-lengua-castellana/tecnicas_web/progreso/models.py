from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Actividad(models.Model):
    """Registro de actividades del usuario"""
    TIPOS = (
        ('visualizacion', 'Visualización'),
        ('completado', 'Completado'),
        ('calificacion', 'Calificación'),
        ('comentario', 'Comentario'),
        ('favorito', 'Favorito'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actividades')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    tecnica = models.ForeignKey('core.Tecnica', on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()} - {self.fecha}"

class Logro(models.Model):
    """Logros que pueden obtener los usuarios"""
    TIPOS = (
        ('estrella', 'Estrella'),
        ('medalla', 'Medalla'),
        ('trofeo', 'Trofeo'),
        ('diploma', 'Diploma'),
    )
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    icono = models.CharField(max_length=50, default='🏆')
    puntos_requeridos = models.IntegerField(default=0)
    tecnicas_requeridas = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"

class LogroUsuario(models.Model):
    """Logros obtenidos por usuarios"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros_obtenidos')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'logro')
        ordering = ['-fecha_obtencion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.logro.nombre}"

class Estadistica(models.Model):
    """Estadísticas del usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estadisticas')
    total_tecnicas_vistas = models.IntegerField(default=0)
    total_tecnicas_completadas = models.IntegerField(default=0)
    total_cursos_inscritos = models.IntegerField(default=0)
    total_cursos_completados = models.IntegerField(default=0)
    tiempo_total_estudio = models.IntegerField(default=0)
    racha_dias = models.IntegerField(default=0)
    ultimo_estudio = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Estadísticas de {self.usuario.username}"
