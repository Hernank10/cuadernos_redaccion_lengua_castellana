from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Curso(models.Model):
    NIVELES = (
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    )
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVELES, default='principiante')
    imagen_url = models.URLField(blank=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)
    duracion_horas = models.IntegerField(default=0)
    tecnicas = models.ManyToManyField('core.Tecnica', blank=True, related_name='cursos')
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    def get_estudiantes_count(self):
        return self.inscripcion_set.count()

class Inscripcion(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    progreso = models.IntegerField(default=0)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    calificacion = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('estudiante', 'curso')
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.titulo}"

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tecnica = models.ForeignKey('core.Tecnica', on_delete=models.SET_NULL, null=True, blank=True)
    orden = models.IntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)
    duracion_minutos = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class ProgresoLeccion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    tiempo_estudio = models.IntegerField(default=0)
    intentos = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('estudiante', 'leccion')
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.leccion.titulo}"

# ============ GAMIFICACIÓN ============
class PuntosUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='puntos_usuario')
    total_puntos = models.IntegerField(default=0)
    racha_dias = models.IntegerField(default=0)
    ultimo_actividad = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.total_puntos} pts"

class Insignia(models.Model):
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
    
    def __str__(self):
        return f"{self.icono} {self.nombre} ({self.nivel})"

class InsigniaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insignias_usuario')
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'insignia')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.insignia.nombre}"

class ActividadUsuario(models.Model):
    TIPOS = (
        ('curso_iniciado', 'Curso Iniciado'),
        ('curso_completado', 'Curso Completado'),
        ('leccion_completada', 'Lección Completada'),
        ('insignia_obtenida', 'Insignia Obtenida'),
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
        return f"{self.usuario.username} - {self.get_tipo_display()}"

# Agregar al final del archivo, después de los modelos existentes

class Certificado(models.Model):
    """Modelo para certificados de cursos completados"""
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados_curso')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='certificados_curso')
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField()
    puntuacion = models.FloatField(default=0.0)
    horas = models.IntegerField(default=0)
    pdf_file = models.FileField(upload_to='certificados/', blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_emision']
        unique_together = ('usuario', 'curso')
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
    
    def __str__(self):
        return f"Certificado - {self.usuario.username} - {self.curso.titulo}"
    
    def generar_codigo(self):
        import hashlib
        import uuid
        data = f"{self.usuario.id}{self.curso.id}{timezone.now().timestamp()}{uuid.uuid4()}"
        codigo = hashlib.sha256(data.encode()).hexdigest()[:12].upper()
        self.codigo = codigo
        return codigo
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.generar_codigo()
        super().save(*args, **kwargs)
    
    def verificar_codigo(self, codigo):
        return self.codigo == codigo

# ============================================
# GAMIFICACIÓN AVANZADA
# ============================================

class NivelUsuario(models.Model):
    """Niveles de usuario con beneficios"""
    NIVELES = [
        (1, '🌱 Novato'),
        (2, '📚 Aprendiz'),
        (3, '🔍 Explorador'),
        (4, '🎓 Conocedor'),
        (5, '⚡ Experto'),
        (6, '🏆 Maestro'),
        (7, '🧠 Sabio'),
        (8, '👑 Leyenda'),
        (9, '🌟 Mítico'),
        (10, '✨ Dios de la Lengua'),
    ]
    
    nivel = models.IntegerField(choices=NIVELES, default=1)
    puntos_necesarios = models.IntegerField()
    icono = models.CharField(max_length=50, default='⭐')
    beneficio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Nivel {self.nivel}: {self.get_nivel_display()}"

class InsigniaAvanzada(models.Model):
    """Insignias con categorías y niveles"""
    CATEGORIAS = [
        ('aprendizaje', '📖 Aprendizaje'),
        ('logro', '🏅 Logro'),
        ('desafio', '⚡ Desafío'),
        ('racha', '🔥 Racha'),
        ('especial', '✨ Especial'),
        ('social', '🤝 Social'),
    ]
    
    NIVELES = [
        ('bronce', '🥉 Bronce'),
        ('plata', '🥈 Plata'),
        ('oro', '🥇 Oro'),
        ('platino', '💎 Platino'),
        ('diamante', '👑 Diamante'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    nivel = models.CharField(max_length=20, choices=NIVELES, default='bronce')
    icono = models.CharField(max_length=50, default='🏆')
    puntos_requeridos = models.IntegerField(default=0)
    cursos_requeridos = models.IntegerField(default=0)
    lecciones_requeridas = models.IntegerField(default=0)
    evaluaciones_aprobadas = models.IntegerField(default=0)
    racha_dias = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.icono} {self.nombre} ({self.nivel})"

class RachaUsuario(models.Model):
    """Seguimiento de rachas de actividad"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='racha')
    racha_actual = models.IntegerField(default=0)
    racha_maxima = models.IntegerField(default=0)
    ultimo_estudio = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.racha_actual} días"

class Desafio(models.Model):
    """Desafíos temporales para los usuarios"""
    TIPOS = [
        ('diario', '📅 Desafío Diario'),
        ('semanal', '📆 Desafío Semanal'),
        ('mensual', '📊 Desafío Mensual'),
        ('especial', '🎯 Desafío Especial'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    puntos_recompensa = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    completado_por = models.ManyToManyField(User, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.titulo} ({self.tipo})"

class LogroUsuario(models.Model):
    """Logros detallados de usuarios"""
    ESTADOS = [
        ('en_progreso', '🔄 En Progreso'),
        ('completado', '✅ Completado'),
        ('reclamado', '🎁 Reclamado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logros_usuario')
    insignia = models.ForeignKey('InsigniaAvanzada', on_delete=models.CASCADE)
    progreso = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_progreso')
    fecha_obtencion = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('usuario', 'insignia')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.insignia.nombre} ({self.estado})"

class EventoGamificacion(models.Model):
    """Registro de eventos de gamificación"""
    TIPOS = [
        ('puntos', '⭐ Puntos Obtenidos'),
        ('insignia', '🏅 Insignia Obtenida'),
        ('nivel', '⬆️ Nivel Alcanzado'),
        ('racha', '🔥 Racha Lograda'),
        ('desafio', '⚡ Desafío Completado'),
        ('logro', '🎯 Logro Alcanzado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_gamificacion')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.CharField(max_length=500)
    puntos = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"
