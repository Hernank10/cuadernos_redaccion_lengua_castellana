from django.contrib import admin
from .models import Evaluacion, Pregunta, RespuestaUsuario, ResultadoEvaluacion

class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1
    fields = ['pregunta', 'tipo', 'opciones', 'respuesta_correcta', 'puntaje', 'orden', 'explicacion']
    ordering = ['orden']

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'tipo', 'publicado', 'fecha_creacion', 'get_total_preguntas']
    list_filter = ['tipo', 'publicado', 'curso']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion']
    inlines = [PreguntaInline]
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'descripcion', 'curso', 'tipo')
        }),
        ('Configuración', {
            'fields': ('duracion_minutos', 'puntaje_maximo', 'publicado', 'fecha_limite')
        }),
    )
    
    def get_total_preguntas(self, obj):
        return obj.get_total_preguntas()
    get_total_preguntas.short_description = 'Total Preguntas'

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'tipo', 'evaluacion', 'puntaje', 'orden']
    list_filter = ['tipo', 'evaluacion']
    search_fields = ['pregunta']

@admin.register(RespuestaUsuario)
class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pregunta', 'calificacion', 'fecha_respuesta']
    list_filter = ['fecha_respuesta']
    search_fields = ['usuario__username']

@admin.register(ResultadoEvaluacion)
class ResultadoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'evaluacion', 'puntaje_obtenido', 'aprobado', 'fecha_completado']
    list_filter = ['aprobado', 'fecha_completado']
    search_fields = ['usuario__username', 'evaluacion__titulo']
