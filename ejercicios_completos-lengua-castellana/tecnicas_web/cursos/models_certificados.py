from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import hashlib
import uuid

User = get_user_model()

class Certificado(models.Model):
    """Modelo para certificados de cursos completados"""
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='certificados')
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
        """Genera un código único para el certificado"""
        data = f"{self.usuario.id}{self.curso.id}{timezone.now().timestamp()}{uuid.uuid4()}"
        codigo = hashlib.sha256(data.encode()).hexdigest()[:12].upper()
        self.codigo = codigo
        return codigo
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.generar_codigo()
        super().save(*args, **kwargs)
    
    def verificar_codigo(self, codigo):
        """Verifica si un código es válido"""
        return self.codigo == codigo
    
    def get_estado(self):
        """Retorna el estado del certificado"""
        if self.pdf_file:
            return 'generado'
        return 'pendiente'
