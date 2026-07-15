from django.db import models
from django.utils.safestring import mark_safe

class Tecnica(models.Model):
    titulo = models.CharField(max_length=500)
    contenido = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=100, db_index=True)
    subcategoria = models.CharField(max_length=100, blank=True, null=True)
    grado = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    ruta_archivo = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['categoria', 'titulo']
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['titulo']),
        ]
    
    def __str__(self):
        return self.titulo[:100]
    
    def get_contenido_html(self):
        """Retorna el contenido como HTML seguro para renderizar"""
        if self.contenido:
            return mark_safe(self.contenido)
        return ""
    
    def get_categoria_display(self):
        categorias = {
            'General': '📚 General',
            'Gramática y Sintaxis': '📖 Gramática y Sintaxis',
            'Ciencia Ficción': '🚀 Ciencia Ficción',
            'Ortografía': '✏️ Ortografía',
            'Educación Colombia': '🇨🇴 Educación Colombia',
            'Literatura y Narrativa': '📝 Literatura y Narrativa',
            'JSON': '📊 JSON',
            'Inglés Bilingüe': '🇬🇧 Inglés Bilingüe',
            'Retórica y Figuras': '🎭 Retórica y Figuras',
            'Cuadernos': '📓 Cuadernos',
            'Redacción Científica': '🔬 Redacción Científica',
            'Comprensión Lectora': '📖 Comprensión Lectora',
        }
        return categorias.get(self.categoria, self.categoria)

class TecnicaJSON(models.Model):
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE, related_name='tecnicas_json')
    tecnica_numero = models.IntegerField()
    titulo_tecnica = models.CharField(max_length=200)
    teoria = models.TextField(blank=True, null=True)
    ejemplo = models.TextField(blank=True, null=True)
    ejercicio = models.TextField(blank=True, null=True)
    respuesta = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['tecnica_numero']
    
    def __str__(self):
        return f"{self.tecnica.titulo[:50]} - Técnica {self.tecnica_numero}"
