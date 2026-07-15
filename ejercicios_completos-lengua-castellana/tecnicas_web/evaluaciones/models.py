from django.db import models
from django.contrib.auth import get_user_model
from cursos.models import Curso

User = get_user_model()

class Evaluacion(models.Model):
    """Modelo de evaluación"""
    TIPOS = (
        ('diagnostico', 'Diagnóstico'),
        ('formativa', 'Formativa'),
        ('sumativa', 'Sumativa'),
        ('final', 'Final'),
    )
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='evaluaciones')
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
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"
    
    def get_total_preguntas(self):
        return self.preguntas.count()
    
    def get_puntaje_total(self):
        return sum(p.puntaje for p in self.preguntas.all())

class Pregunta(models.Model):
    """Modelo de pregunta"""
    TIPOS = (
        ('multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
        ('completar', 'Completar'),
        ('abierta', 'Pregunta Abierta'),
    )
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    pregunta = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='multiple')
    opciones = models.JSONField(default=list, blank=True, help_text='Para opción múltiple: ["Opción A", "Opción B", ...]')
    respuesta_correcta = models.TextField(help_text='Para múltiple: índice (0,1,2...). Para V/F: "V" o "F"')
    puntaje = models.FloatField(default=1.0)
    orden = models.IntegerField(default=0)
    explicacion = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
    
    def __str__(self):
        return f"{self.evaluacion.titulo} - Pregunta {self.orden}"

class RespuestaUsuario(models.Model):
    """Modelo de respuestas de usuarios"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas_evaluaciones')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.TextField()
    calificacion = models.FloatField(default=0.0)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'pregunta')
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.pregunta[:30]}"

class ResultadoEvaluacion(models.Model):
    """Modelo de resultados de evaluaciones"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultados_evaluaciones')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    puntaje_obtenido = models.FloatField(default=0.0)
    aprobado = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    intentos = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('usuario', 'evaluacion')
        verbose_name = 'Resultado'
        verbose_name_plural = 'Resultados'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.evaluacion.titulo}: {self.puntaje_obtenido}%"
