from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PuntosUsuario, ActividadUsuario, InsigniaUsuario, Insignia

@login_required
def gamificacion(request):
    puntos_usuario, _ = PuntosUsuario.objects.get_or_create(usuario=request.user)
    actividades = ActividadUsuario.objects.filter(usuario=request.user)[:20]
    insignias = InsigniaUsuario.objects.filter(usuario=request.user)
    todas_insignias = Insignia.objects.all()
    
    context = {
        'puntos_usuario': puntos_usuario,
        'actividades': actividades,
        'insignias': insignias,
        'todas_insignias': todas_insignias,
        'total_insignias': insignias.count(),
        'total_actividades': ActividadUsuario.objects.filter(usuario=request.user).count(),
        'titulo': 'Gamificación'
    }
    return render(request, 'cursos/gamificacion.html', context)

@login_required
def ranking(request):
    top_usuarios = PuntosUsuario.objects.filter(total_puntos__gt=0).order_by('-total_puntos')[:10]
    
    puntos_usuario, _ = PuntosUsuario.objects.get_or_create(usuario=request.user)
    posicion = PuntosUsuario.objects.filter(total_puntos__gt=puntos_usuario.total_puntos).count() + 1
    
    context = {
        'top_usuarios': top_usuarios,
        'posicion': posicion,
        'puntos_usuario': puntos_usuario,
        'titulo': 'Ranking'
    }
    return render(request, 'cursos/ranking.html', context)
