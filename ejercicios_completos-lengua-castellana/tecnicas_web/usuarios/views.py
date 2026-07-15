from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Usuario, PerfilEstudiante, PerfilProfesor
from core.models import Tecnica
from cursos.models import Curso, Inscripcion, ProgresoLeccion

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        rol = request.POST.get('rol', 'estudiante')
        
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'usuarios/registro.html')
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'usuarios/registro.html')
        
        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            rol=rol
        )
        
        login(request, usuario)
        messages.success(request, f'¡Bienvenido {username}!')
        return redirect('core:index')
    
    return render(request, 'usuarios/registro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f'¡Bienvenido de vuelta {username}!')
            return redirect('core:index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('core:index')

@login_required
def perfil(request):
    usuario = request.user
    context = {
        'usuario': usuario,
        'titulo': 'Mi Perfil'
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def progreso(request):
    usuario = request.user
    
    # Técnicas vistas (contar desde Tecnica)
    tecnicas_vistas = Tecnica.objects.count()  # Simplificado
    
    # Cursos en progreso
    cursos_en_progreso = Inscripcion.objects.filter(estudiante=usuario, estado='activo')
    
    # Lecciones completadas
    lecciones_completadas = ProgresoLeccion.objects.filter(
        estudiante=usuario, 
        completado=True
    ).count()
    
    context = {
        'tecnicas_vistas': tecnicas_vistas,
        'cursos_en_progreso': cursos_en_progreso,
        'lecciones_completadas': lecciones_completadas,
        'titulo': 'Mi Progreso'
    }
    return render(request, 'usuarios/progreso.html', context)

@login_required
def favoritos(request):
    # Simplificado - mostrar técnicas como favoritas
    tecnicas = Tecnica.objects.all()[:10]
    context = {
        'favoritos': tecnicas,
        'titulo': 'Mis Favoritos'
    }
    return render(request, 'usuarios/favoritos.html', context)
