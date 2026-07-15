from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilEstudiante, PerfilProfesor

class PerfilEstudianteInline(admin.StackedInline):
    model = PerfilEstudiante
    can_delete = False
    verbose_name_plural = 'Perfil Estudiante'

class PerfilProfesorInline(admin.StackedInline):
    model = PerfilProfesor
    can_delete = False
    verbose_name_plural = 'Perfil Profesor'

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'rol', 'is_superuser', 'fecha_registro', 'puntos', 'nivel']
    list_filter = ['rol', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['fecha_registro', 'ultimo_acceso']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'fecha_nacimiento')}),
        ('Información de la Cuenta', {'fields': ('rol', 'puntos', 'nivel')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('fecha_registro', 'ultimo_acceso')}),
        ('Perfil', {'fields': ('avatar_url', 'bio')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol'),
        }),
    )
    
    inlines = [PerfilEstudianteInline, PerfilProfesorInline]

@admin.register(PerfilEstudiante)
class PerfilEstudianteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'promedio_calificacion', 'horas_estudio']
    search_fields = ['usuario__username']

@admin.register(PerfilProfesor)
class PerfilProfesorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad', 'experiencia']
    search_fields = ['usuario__username']
