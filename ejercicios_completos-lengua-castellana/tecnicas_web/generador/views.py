from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from cursos.models import Curso
from evaluaciones.models import Evaluacion

@staff_member_required
def dashboard_generador(request):
    """Panel de control del generador de evaluaciones"""
    cursos = Curso.objects.filter(publicado=True)
    evaluaciones = Evaluacion.objects.all().order_by('-fecha_creacion')[:10]
    
    context = {
        'cursos': cursos,
        'evaluaciones': evaluaciones,
        'total_evaluaciones': Evaluacion.objects.count(),
        'total_cursos': cursos.count(),
        'titulo': 'Generador de Evaluaciones'
    }
    return render(request, 'generador/dashboard.html', context)

@staff_member_required
def generar_evaluacion(request):
    """Genera una nueva evaluación"""
    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        num_preguntas = int(request.POST.get('num_preguntas', 10))
        tipo = request.POST.get('tipo', 'curso')
        
        # Importar aquí para evitar problemas de importación circular
        from .generador_evaluaciones import GeneradorEvaluaciones
        generador = GeneradorEvaluaciones()
        
        if tipo == 'curso' and curso_id:
            curso = Curso.objects.filter(id=curso_id).first()
            if curso:
                evaluacion = generador.generar_evaluacion_para_curso(curso, num_preguntas)
                if evaluacion:
                    messages.success(request, f'✅ Evaluación "{evaluacion.titulo}" creada exitosamente')
                else:
                    messages.error(request, '❌ No se pudo generar la evaluación')
            else:
                messages.error(request, '❌ Curso no encontrado')
        
        elif tipo == 'rapida':
            evaluacion = generador.generar_evaluacion_rapida(num_preguntas)
            if evaluacion:
                messages.success(request, f'✅ Evaluación rápida "{evaluacion.titulo}" creada')
            else:
                messages.error(request, '❌ No se pudo generar la evaluación rápida')
        
        elif tipo == 'categoria':
            categoria = request.POST.get('categoria')
            if categoria:
                evaluacion = generador.generar_por_categoria(categoria, num_preguntas)
                if evaluacion:
                    messages.success(request, f'✅ Evaluación para "{categoria}" creada')
                else:
                    messages.error(request, f'❌ No se encontraron técnicas en "{categoria}"')
    
    return redirect('generador:dashboard')
