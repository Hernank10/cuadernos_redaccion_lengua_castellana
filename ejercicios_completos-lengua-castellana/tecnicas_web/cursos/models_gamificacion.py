from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# ============ CERTIFICADOS ============
class Certificado(models.Model):
    """Modelo para certificados de cursos completados"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField()
    puntuacion = models.FloatField(default=0.0)
    pdf_file = models.FileField(upload_to='certificados/', blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_emision']
        unique_together = ('usuario', 'curso')
    
    def __str__(self):
        return f"Certificado - {self.usuario.username} - {self.curso.titulo}"
    
    def generar_codigo(self):
        import hashlib
        import time
        data = f"{self.usuario.id}{self.curso.id}{time.time()}"
        return hashlib.md5(data.encode()).hexdigest()[:10].upper()

# ============ EVALUACIONES ============
class Evaluacion(models.Model):
    """Modelo para evaluaciones de cursos"""
    TIPOS = (
        ('diagnostico', 'Diagnóstico'),
        ('formativa', 'Formativa'),
        ('sumativa', 'Sumativa'),
        ('final', 'Final'),
    )
    
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='evaluaciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='formativa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(blank=True, null=True)
    duracion_minutos = models.IntegerField(default=30)
    puntaje_maximo = models.FloatField(default=100)
    publicado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Pregunta(models.Model):
    """Modelo para preguntas de evaluaciones"""
    TIPOS = (
        ('multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('completar', 'Completar'),
        ('abierta', 'Pregunta Abierta'),
    )
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    pregunta = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='multiple')
    opciones = models.JSONField(default=list, blank=True)  # Para opción múltiple
    respuesta_correcta = models.TextField()
    puntaje = models.FloatField(default=1.0)
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.evaluacion.titulo} - Pregunta {self.orden}"

class RespuestaUsuario(models.Model):
    """Modelo para respuestas de usuarios en evaluaciones"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.TextField()
    calificacion = models.FloatField(default=0.0)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'pregunta')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.pregunta[:30]}"

class ResultadoEvaluacion(models.Model):
    """Modelo para resultados de evaluaciones"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultados_evaluaciones')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    puntaje_obtenido = models.FloatField(default=0.0)
    aprobado = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    intentos = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('usuario', 'evaluacion')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.evaluacion.titulo}: {self.puntaje_obtenido}%"

# ============ GAMIFICACIÓN ============
class Insignia(models.Model):
    """Modelo para insignias/logros"""
    NIVELES = (
        ('bronce', 'Bronce'),
        ('plata', 'Plata'),
        ('oro', 'Oro'),
        ('platino', 'Platino'),
        ('diamante', 'Diamante'),
    )
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVELES, default='bronce')
    icono = models.CharField(max_length=50, default='🏆')
    puntos_requeridos = models.IntegerField(default=0)
    cursos_requeridos = models.IntegerField(default=0)
    tecnicas_requeridas = models.IntegerField(default=0)
    criterios = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.icono} {self.nombre} ({self.nivel})"

class InsigniaUsuario(models.Model):
    """Modelo para insignias obtenidas por usuarios"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insignias')
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'insignia')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.insignia.nombre}"

class PuntosUsuario(models.Model):
    """Modelo para puntos acumulados por usuarios"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='puntos')
    total_puntos = models.IntegerField(default=0)
    puntos_curso = models.JSONField(default=dict, blank=True)  # {curso_id: puntos}
    racha_dias = models.IntegerField(default=0)
    ultimo_actividad = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.total_puntos} puntos"
    
    def agregar_puntos(self, cantidad, curso_id=None):
        """Agrega puntos al usuario"""
        self.total_puntos += cantidad
        if curso_id:
            curso_key = str(curso_id)
            self.puntos_curso[curso_key] = self.puntos_curso.get(curso_key, 0) + cantidad
        self.save()
    
    def verificar_insignias(self):
        """Verifica si el usuario ha obtenido nuevas insignias"""
        from .models import Insignia, InsigniaUsuario
        from django.db.models import Count
        
        # Contar cursos completados
        cursos_completados = self.usuario.inscripcion_set.filter(estado='completado').count()
        tecnicas_completadas = self.usuario.perfil_estudiante.tecnicas_completadas.count()
        
        # Buscar insignias disponibles
        insignias_disponibles = Insignia.objects.filter(
            puntos_requeridos__lte=self.total_puntos,
            cursos_requeridos__lte=cursos_completados,
            tecnicas_requeridas__lte=tecnicas_completadas
        ).exclude(id__in=self.usuario.insignias.values_list('insignia_id', flat=True))
        
        nuevas_insignias = []
        for insignia in insignias_disponibles:
            InsigniaUsuario.objects.create(usuario=self.usuario, insignia=insignia)
            nuevas_insignias.append(insignia)
        
        return nuevas_insignias

class ActividadUsuario(models.Model):
    """Modelo para registrar actividades del usuario (gamificación)"""
    TIPOS = (
        ('curso_iniciado', 'Curso Iniciado'),
        ('curso_completado', 'Curso Completado'),
        ('leccion_completada', 'Lección Completada'),
        ('evaluacion_aprobada', 'Evaluación Aprobada'),
        ('insignia_obtenida', 'Insignia Obtenida'),
        ('tecnica_vista', 'Técnica Vista'),
        ('puntos_obtenidos', 'Puntos Obtenidos'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actividades_gamificacion')
    tipo = models.CharField(max_length=30, choices=TIPOS)
    descripcion = models.CharField(max_length=500)
    puntos = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()} - {self.fecha}"
