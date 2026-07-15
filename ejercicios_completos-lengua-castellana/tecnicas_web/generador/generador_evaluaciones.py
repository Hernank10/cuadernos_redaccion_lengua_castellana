"""
Generador Automático de Evaluaciones - Versión Corregida
"""

import random
import re
from datetime import datetime
from django.db.models import Q

from core.models import Tecnica
from cursos.models import Curso
from evaluaciones.models import Evaluacion, Pregunta
from usuarios.models import Usuario

class GeneradorEvaluaciones:
    """Generador automático de evaluaciones"""
    
    def __init__(self):
        self.tecnicas = Tecnica.objects.all()
        self.cursos = Curso.objects.filter(publicado=True)
        self.admin = Usuario.objects.filter(is_superuser=True).first()
        self.evaluaciones_creadas = 0
        self.preguntas_creadas = 0
        
        print(f"📚 Técnicas disponibles: {self.tecnicas.count()}")
        print(f"📖 Cursos disponibles: {self.cursos.count()}")
        print(f"👤 Admin: {self.admin.username if self.admin else 'No encontrado'}")
    
    def generar_evaluacion_para_curso(self, curso, num_preguntas=10, titulo=None):
        """Genera una evaluación para un curso"""
        if not curso or not self.admin:
            return None
        
        print(f"\n📝 Generando evaluación para: {curso.titulo}")
        
        # Buscar preguntas existentes del curso
        preguntas_existentes = Pregunta.objects.filter(
            evaluacion__curso=curso
        ).order_by('?')[:num_preguntas]
        
        preguntas_lista = list(preguntas_existentes)
        
        # Si no hay suficientes, buscar preguntas de otras evaluaciones
        if len(preguntas_lista) < num_preguntas:
            print(f"   ⚠️ Solo {len(preguntas_lista)} preguntas existentes. Buscando más...")
            
            # Buscar preguntas de otras evaluaciones
            preguntas_adicionales = Pregunta.objects.exclude(
                evaluacion__curso=curso
            ).order_by('?')[:num_preguntas - len(preguntas_lista)]
            
            preguntas_lista.extend(list(preguntas_adicionales))
        
        # Si aún no hay suficientes, crear preguntas genéricas
        if len(preguntas_lista) < num_preguntas:
            print(f"   ⚠️ Creando preguntas genéricas...")
            
            # Crear preguntas de ejemplo
            preguntas_ejemplo = [
                {'pregunta': '¿Qué es un sustantivo?', 'tipo': 'multiple', 
                 'opciones': ['Persona', 'Lugar', 'Cosa', 'Todos los anteriores'], 
                 'respuesta_correcta': '3', 'puntaje': 10},
                {'pregunta': 'El verbo indica acción o estado.', 'tipo': 'verdadero_falso',
                 'opciones': ['Verdadero', 'Falso'], 'respuesta_correcta': 'V', 'puntaje': 5},
                {'pregunta': 'Los ___________ son palabras que unen oraciones.', 'tipo': 'completar',
                 'opciones': [], 'respuesta_correcta': 'conectores', 'puntaje': 5},
                {'pregunta': '¿Qué función cumplen los signos de puntuación?', 'tipo': 'abierta',
                 'opciones': [], 'respuesta_correcta': 'Organizar y dar claridad al texto', 'puntaje': 10},
            ]
            
            for data in preguntas_ejemplo[:num_preguntas - len(preguntas_lista)]:
                # Crear evaluación temporal si no existe
                eval_temp, _ = Evaluacion.objects.get_or_create(
                    titulo="Preguntas de Ejemplo",
                    defaults={
                        'curso': curso,
                        'tipo': 'formativa',
                        'publicado': True
                    }
                )
                
                nueva_pregunta = Pregunta.objects.create(
                    evaluacion=eval_temp,
                    pregunta=data['pregunta'],
                    tipo=data['tipo'],
                    opciones=data.get('opciones', []),
                    respuesta_correcta=data['respuesta_correcta'],
                    puntaje=data.get('puntaje', 5)
                )
                preguntas_lista.append(nueva_pregunta)
                print(f"   ✅ Creada: {nueva_pregunta.pregunta[:40]}...")
        
        if not preguntas_lista:
            print("   ❌ No se encontraron preguntas")
            return None
        
        # Seleccionar preguntas
        random.shuffle(preguntas_lista)
        preguntas_seleccionadas = preguntas_lista[:num_preguntas]
        
        # Crear evaluación
        evaluacion_titulo = titulo or f"Evaluación: {curso.titulo[:40]}"
        evaluacion = Evaluacion.objects.create(
            curso=curso,
            titulo=evaluacion_titulo,
            descripcion=f"Evaluación automática con {len(preguntas_seleccionadas)} preguntas",
            tipo='formativa',
            duracion_minutos=max(10, len(preguntas_seleccionadas) * 2),
            puntaje_maximo=sum(p.puntaje for p in preguntas_seleccionadas),
            publicado=True
        )
        
        # Copiar preguntas a la nueva evaluación
        for i, pregunta_original in enumerate(preguntas_seleccionadas, 1):
            Pregunta.objects.create(
                evaluacion=evaluacion,
                pregunta=pregunta_original.pregunta,
                tipo=pregunta_original.tipo,
                opciones=pregunta_original.opciones,
                respuesta_correcta=pregunta_original.respuesta_correcta,
                puntaje=pregunta_original.puntaje,
                orden=i,
                explicacion=pregunta_original.explicacion
            )
            self.preguntas_creadas += 1
        
        self.evaluaciones_creadas += 1
        print(f"\n✅ Evaluación creada: {evaluacion.titulo}")
        print(f"   Preguntas: {len(preguntas_seleccionadas)}")
        print(f"   Duración: {evaluacion.duracion_minutos} min")
        print(f"   Puntaje: {evaluacion.puntaje_maximo}")
        
        return evaluacion
    
    def generar_para_todos_los_cursos(self, preguntas_por_curso=10):
        """Genera evaluaciones para todos los cursos"""
        print("\n" + "="*60)
        print("🚀 GENERANDO EVALUACIONES PARA TODOS LOS CURSOS")
        print("="*60)
        
        for curso in self.cursos:
            self.generar_evaluacion_para_curso(curso, preguntas_por_curso)
        
        print(f"\n📊 Total evaluaciones creadas: {self.evaluaciones_creadas}")
        print(f"📝 Total preguntas creadas: {self.preguntas_creadas}")
    
    def generar_evaluacion_rapida(self, num_preguntas=10):
        """Genera una evaluación rápida con preguntas variadas"""
        print("\n" + "="*60)
        print("⚡ GENERANDO EVALUACIÓN RÁPIDA")
        print("="*60)
        
        # Buscar preguntas existentes
        preguntas_existentes = Pregunta.objects.all().order_by('?')[:num_preguntas]
        preguntas_lista = list(preguntas_existentes)
        
        if len(preguntas_lista) < num_preguntas:
            print(f"⚠️ Solo hay {len(preguntas_lista)} preguntas. Creando más...")
        
        # Crear curso temporal
        curso, _ = Curso.objects.get_or_create(
            titulo="Evaluación Rápida - Técnicas Generales",
            defaults={
                'descripcion': "Evaluación rápida con preguntas variadas",
                'creador': self.admin,
                'publicado': True,
                'nivel': 'intermedio',
                'duracion_horas': 5
            }
        )
        
        return self.generar_evaluacion_para_curso(curso, num_preguntas, "Evaluación Rápida - Técnicas Generales")
    
    def generar_por_categoria(self, categoria, num_preguntas=10):
        """Genera evaluación por categoría"""
        tecnicas_categoria = self.tecnicas.filter(categoria__icontains=categoria)
        if not tecnicas_categoria:
            print(f"⚠️ No se encontraron técnicas en '{categoria}'")
            return None
        
        curso, _ = Curso.objects.get_or_create(
            titulo=f"Curso: {categoria}",
            defaults={
                'descripcion': f"Curso automático para {categoria}",
                'creador': self.admin,
                'publicado': True,
                'nivel': 'intermedio'
            }
        )
        curso.tecnicas.add(*tecnicas_categoria[:20])
        
        return self.generar_evaluacion_para_curso(curso, num_preguntas, f"Evaluación - {categoria}")

def _crear_pregunta_ordenar(self):
    """Crea una pregunta de ordenar"""
    return {
        'pregunta': 'Ordena los siguientes elementos correctamente:',
        'tipo': 'ordenar',
        'opciones': ['Primero', 'Segundo', 'Tercero', 'Cuarto'],
        'respuesta_correcta': '0,1,2,3',
        'puntaje': 10
    }

def _crear_pregunta_relacionar(self):
    """Crea una pregunta de relacionar"""
    return {
        'pregunta': 'Relaciona cada concepto con su definición:',
        'tipo': 'relacionar',
        'opciones': ['Concepto A', 'Concepto B', 'Concepto C'],
        'respuesta_correcta': '0-1,1-2,2-0',
        'puntaje': 10
    }
