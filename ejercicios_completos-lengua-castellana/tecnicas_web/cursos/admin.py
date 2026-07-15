from django.contrib import admin
from .models import Curso, Leccion, Inscripcion, ProgresoLeccion

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'creador', 'nivel', 'publicado', 'fecha_creacion']
    list_filter = ['nivel', 'publicado']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    filter_horizontal = ['tecnicas']

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'orden', 'duracion_minutos']
    list_filter = ['curso']
    search_fields = ['titulo', 'descripcion']

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'estado', 'progreso']
    list_filter = ['estado', 'curso']
    search_fields = ['estudiante__username', 'curso__titulo']

@admin.register(ProgresoLeccion)
class ProgresoLeccionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'leccion', 'completado']
    list_filter = ['completado']
    search_fields = ['estudiante__username', 'leccion__titulo']
