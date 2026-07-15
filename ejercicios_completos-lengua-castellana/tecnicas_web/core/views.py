from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Tecnica

def index(request):
    total_tecnicas = Tecnica.objects.count()
    total_categorias = Tecnica.objects.values('categoria').distinct().count()
    
    categorias = Tecnica.objects.values('categoria').annotate(
        total=Count('categoria')
    ).order_by('-total')
    
    ultimas = Tecnica.objects.all().order_by('-id')[:10]
    
    context = {
        'total_tecnicas': total_tecnicas,
        'total_categorias': total_categorias,
        'categorias': categorias,
        'ultimas': ultimas,
        'titulo': 'Inicio - Técnicas de Lengua Castellana'
    }
    return render(request, 'core/index.html', context)

def tecnicas_list(request):
    tecnicas = Tecnica.objects.all()
    
    categoria = request.GET.get('categoria')
    if categoria:
        tecnicas = tecnicas.filter(categoria=categoria)
    
    q = request.GET.get('q')
    if q:
        tecnicas = tecnicas.filter(
            Q(titulo__icontains=q) | Q(contenido__icontains=q)
        )
    
    paginator = Paginator(tecnicas, 20)
    page = request.GET.get('page')
    tecnicas_page = paginator.get_page(page)
    
    categorias = Tecnica.objects.values_list('categoria', flat=True).distinct()
    
    context = {
        'tecnicas': tecnicas_page,
        'categorias': categorias,
        'categoria_actual': categoria,
        'q': q,
        'titulo': 'Todas las técnicas'
    }
    return render(request, 'core/tecnicas_list.html', context)

def tecnica_detail(request, pk):
    """Sirve el archivo HTML completo tal como está"""
    tecnica = get_object_or_404(Tecnica, pk=pk)
    
    # Si tiene contenido, devolverlo directamente como HTML
    if tecnica.contenido:
        return HttpResponse(tecnica.contenido, content_type='text/html; charset=utf-8')
    
    # Si no tiene contenido, mostrar un mensaje
    return HttpResponse(f"<h1>{tecnica.titulo}</h1><p>No hay contenido disponible</p>", content_type='text/html; charset=utf-8')

def categorias(request):
    categorias_data = []
    for cat in Tecnica.objects.values('categoria').annotate(
        total=Count('categoria')
    ).order_by('categoria'):
        muestras = Tecnica.objects.filter(categoria=cat['categoria'])[:5]
        categorias_data.append({
            'nombre': cat['categoria'],
            'total': cat['total'],
            'muestras': muestras
        })
    
    context = {
        'categorias': categorias_data,
        'titulo': 'Categorías'
    }
    return render(request, 'core/categorias.html', context)

def buscar(request):
    q = request.GET.get('q', '')
    resultados = []
    
    if q:
        resultados = Tecnica.objects.filter(
            Q(titulo__icontains=q) | 
            Q(contenido__icontains=q) |
            Q(categoria__icontains=q)
        )
    
    context = {
        'q': q,
        'resultados': resultados,
        'titulo': f'Resultados para "{q}"'
    }
    return render(request, 'core/buscar.html', context)
