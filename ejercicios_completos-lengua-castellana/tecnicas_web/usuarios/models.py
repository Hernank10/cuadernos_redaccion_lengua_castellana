from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    """Modelo extendido de usuario"""
    ROLES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    puntos = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
    
    def es_estudiante(self):
        return self.rol == 'estudiante'
    
    def es_profesor(self):
        return self.rol == 'profesor'
    
    def es_admin(self):
        return self.rol == 'admin' or self.is_superuser

class PerfilEstudiante(models.Model):
    """Perfil específico para estudiantes"""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_estudiante')
    tecnicas_completadas = models.ManyToManyField('core.Tecnica', blank=True)
    promedio_calificacion = models.FloatField(default=0.0)
    horas_estudio = models.IntegerField(default=0)
    logros = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"

class PerfilProfesor(models.Model):
    """Perfil específico para profesores"""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_profesor')
    especialidad = models.CharField(max_length=200, blank=True, null=True)
    experiencia = models.IntegerField(default=0)
    calificacion_promedio = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Profesor {self.usuario.username}"
