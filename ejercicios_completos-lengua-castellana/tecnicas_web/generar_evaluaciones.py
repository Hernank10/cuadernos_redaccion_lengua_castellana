#!/usr/bin/env python3
"""
Generador Automático de Evaluaciones para LMS Lengua Castellana
Extrae preguntas de las técnicas y crea evaluaciones automáticas
"""

import os
import sys
import json
import re
import random
import django
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica
from cursos.models import Curso
from evaluaciones.models import Evaluacion, Pregunta
from usuarios.models import Usuario

class GeneradorEvaluaciones:
    """Generador automático de evaluaciones basado en técnicas existentes"""
    
    def __init__(self):
        self.tecnicas = Tecnica.objects.all()
        self.cursos = Curso.objects.filter(publicado=True)
        self.admin = Usuario.objects.filter(is_superuser=True).first()
        self.evaluaciones_creadas = 0
        self.preguntas_creadas = 0
        
        print("="*60)
        print("🧠 GENERADOR AUTOMÁTICO DE EVALUACIONES")
        print("="*60)
        print(f"📚 Técnicas disponibles: {self.tecnicas.count()}")
        print(f"📖 Cursos disponibles: {self.cursos.count()}")
        print(f"👤 Admin: {self.admin.username if self.admin else 'No encontrado'}")
        print("="*60)
    
    def extraer_preguntas_del_html(self, contenido_html):
        """Extrae preguntas del contenido HTML de una técnica"""
        preguntas = []
        
        if not contenido_html:
            return preguntas
        
        # Buscar JSON en el HTML
        patron_json = r'```json\s*(\{.*?\})\s*```|```\s*(\{.*?\})\s*```|(\{.*?"preguntas".*?\})|(\{.*?"ejercicios".*?\})'
        matches = re.findall(patron_json, contenido_html, re.DOTALL)
        
        for match in matches:
            for grupo in match:
                if grupo and len(grupo) > 50:
                    try:
                        datos = json.loads(grupo)
                        if isinstance(datos, dict):
                            # Buscar preguntas en diferentes claves
                            for key in ['preguntas', 'ejercicios', 'items', 'cuestionario', 'quiz', 'flashcards']:
                                if key in datos and isinstance(datos[key], list):
                                    for item in datos[key]:
                                        if isinstance(item, dict):
                                            pregunta = self._procesar_item_pregunta(item)
                                            if pregunta:
                                                preguntas.append(pregunta)
                                    break
                    except:
                        pass
        
        # Si no se encontró JSON, buscar con BeautifulSoup
        if not preguntas and len(contenido_html) > 200:
            preguntas.extend(self._extraer_preguntas_con_bs4(contenido_html))
        
        return preguntas
    
    def _procesar_item_pregunta(self, item):
        """Procesa un item para convertir en pregunta"""
        pregunta = {}
        
        # Buscar texto de pregunta
        pregunta['texto'] = item.get('pregunta', item.get('titulo', item.get('texto', '')))
        if not pregunta['texto']:
            return None
        
        # Determinar tipo de pregunta
        if 'opciones' in item and isinstance(item['opciones'], list) and len(item['opciones']) > 1:
            pregunta['tipo'] = 'multiple'
            pregunta['opciones'] = item['opciones']
            pregunta['respuesta'] = str(item.get('respuesta', item.get('correcta', '0')))
        elif 'respuesta_correcta' in item or 'correcta' in item:
            pregunta['tipo'] = 'verdadero_falso'
            pregunta['opciones'] = ['Verdadero', 'Falso']
            pregunta['respuesta'] = 'V' if item.get('respuesta_correcta', item.get('correcta', 'V')) else 'F'
        elif 'completar' in item:
            pregunta['tipo'] = 'completar'
            pregunta['opciones'] = []
            pregunta['respuesta'] = item.get('completar', '')
        else:
            pregunta['tipo'] = 'abierta'
            pregunta['opciones'] = []
            pregunta['respuesta'] = item.get('respuesta', '')
        
        # Puntaje
        pregunta['puntaje'] = item.get('puntaje', 1)
        
        return pregunta
    
    def _extraer_preguntas_con_bs4(self, contenido_html):
        """Extrae preguntas usando BeautifulSoup"""
        preguntas = []
        try:
            soup = BeautifulSoup(contenido_html, 'html.parser')
            
            # Buscar elementos que pueden contener preguntas
            elementos = soup.find_all(['div', 'section', 'article', 'li'], 
                                      class_=re.compile(r'(pregunta|cuestion|quiz|ejercicio|flashcard|card)', re.I))
            
            for elem in elementos[:50]:
                texto = elem.get_text(strip=True)
                if len(texto) > 30:
                    preguntas.append({
                        'texto': texto[:500],
                        'tipo': 'abierta',
                        'opciones': [],
                        'respuesta': 'Respuesta basada en el contenido',
                        'puntaje': 1
                    })
        except:
            pass
        
        return preguntas
    
    def generar_evaluacion_por_curso(self, curso, num_preguntas=10, titulo=None):
        """Genera una evaluación para un curso específico"""
        if not curso or not self.admin:
            return None
        
        # Obtener técnicas del curso
        tecnicas_curso = curso.tecnicas.all()
        if not tecnicas_curso:
            print(f"⚠️ El curso '{curso.titulo}' no tiene técnicas asociadas")
            return None
        
        print(f"\n📝 Generando evaluación para: {curso.titulo}")
        print(f"   Técnicas disponibles: {tecnicas_curso.count()}")
        
        # Extraer preguntas de todas las técnicas del curso
        todas_preguntas = []
        for tecnica in tecnicas_curso[:10]:  # Limitar a 10 técnicas para no sobrecargar
            preguntas = self.extraer_preguntas_del_html(tecnica.contenido)
            if preguntas:
                print(f"   ✅ {tecnica.titulo[:50]}... → {len(preguntas)} preguntas")
                todas_preguntas.extend(preguntas)
        
        if not todas_preguntas:
            print(f"   ⚠️ No se encontraron preguntas en las técnicas del curso")
            return None
        
        # Seleccionar preguntas aleatorias
        random.shuffle(todas_preguntas)
        preguntas_seleccionadas = todas_preguntas[:num_preguntas]
        
        # Crear evaluación
        evaluacion_titulo = titulo or f"Evaluación Automática - {curso.titulo[:30]}"
        evaluacion = Evaluacion.objects.create(
            curso=curso,
            titulo=evaluacion_titulo,
            descripcion=f"Evaluación generada automáticamente basada en {len(preguntas_seleccionadas)} preguntas del curso",
            tipo='formativa',
            duracion_minutos=min(30, len(preguntas_seleccionadas) * 2),
            puntaje_maximo=sum(p.get('puntaje', 1) for p in preguntas_seleccionadas),
            publicado=True
        )
        
        # Guardar preguntas
        for i, p_data in enumerate(preguntas_seleccionadas, 1):
            Pregunta.objects.create(
                evaluacion=evaluacion,
                pregunta=p_data.get('texto', f'Pregunta {i}')[:500],
                tipo=p_data.get('tipo', 'abierta'),
                opciones=p_data.get('opciones', []),
                respuesta_correcta=str(p_data.get('respuesta', '')),
                puntaje=p_data.get('puntaje', 1),
                orden=i
            )
        
        print(f"\n✅ Evaluación creada: {evaluacion.titulo}")
        print(f"   Preguntas: {len(preguntas_seleccionadas)}")
        print(f"   Duración: {evaluacion.duracion_minutos} min")
        print(f"   Puntaje máximo: {evaluacion.puntaje_maximo}")
        
        self.evaluaciones_creadas += 1
        self.preguntas_creadas += len(preguntas_seleccionadas)
        
        return evaluacion
    
    def generar_evaluaciones_para_todos_cursos(self, preguntas_por_curso=10):
        """Genera evaluaciones para todos los cursos"""
        print("\n" + "="*60)
        print("🚀 GENERANDO EVALUACIONES PARA TODOS LOS CURSOS")
        print("="*60)
        
        for curso in self.cursos:
            self.generar_evaluacion_por_curso(curso, preguntas_por_curso)
        
        print("\n" + "="*60)
        print(f"📊 RESUMEN FINAL")
        print(f"   Evaluaciones creadas: {self.evaluaciones_creadas}")
        print(f"   Preguntas creadas: {self.preguntas_creadas}")
        print("="*60)
    
    def generar_evaluacion_por_categoria(self, categoria, num_preguntas=10):
        """Genera una evaluación basada en una categoría específica"""
        tecnicas_categoria = self.tecnicas.filter(categoria__icontains=categoria)
        
        if not tecnicas_categoria:
            print(f"⚠️ No se encontraron técnicas en la categoría: {categoria}")
            return None
        
        # Crear curso temporal si no existe
        curso, _ = Curso.objects.get_or_create(
            titulo=f"Curso: {categoria}",
            defaults={
                'descripcion': f"Curso automático para la categoría {categoria}",
                'creador': self.admin,
                'publicado': True,
                'nivel': 'intermedio',
                'duracion_horas': 10
            }
        )
        curso.tecnicas.add(*tecnicas_categoria[:20])
        
        titulo = f"Evaluación - {categoria}"
        return self.generar_evaluacion_por_curso(curso, num_preguntas, titulo)
    
    def generar_evaluacion_rapida(self, num_preguntas=10):
        """Genera una evaluación rápida con preguntas aleatorias de todas las técnicas"""
        print("\n" + "="*60)
        print("⚡ GENERANDO EVALUACIÓN RÁPIDA")
        print("="*60)
        
        # Seleccionar técnicas aleatorias
        tecnicas_seleccionadas = random.sample(list(self.tecnicas), min(20, len(self.tecnicas)))
        
        todas_preguntas = []
        for tecnica in tecnicas_seleccionadas:
            preguntas = self.extraer_preguntas_del_html(tecnica.contenido)
            if preguntas:
                todas_preguntas.extend(preguntas)
        
        if not todas_preguntas:
            print("❌ No se encontraron preguntas")
            return None
        
        # Seleccionar preguntas
        random.shuffle(todas_preguntas)
        preguntas_seleccionadas = todas_preguntas[:num_preguntas]
        
        # Crear curso temporal
        curso, _ = Curso.objects.get_or_create(
            titulo="Evaluación Rápida - Técnicas Generales",
            defaults={
                'descripcion': "Evaluación rápida con preguntas de todas las técnicas",
                'creador': self.admin,
                'publicado': True,
                'nivel': 'intermedio',
                'duracion_horas': 5
            }
        )
        
        titulo = f"Evaluación Rápida - {datetime.now().strftime('%d/%m/%Y')}"
        return self.generar_evaluacion_por_curso(curso, num_preguntas, titulo)

def main():
    """Función principal"""
    generador = GeneradorEvaluaciones()
    
    print("\n📋 ¿Qué deseas hacer?")
    print("1. Generar evaluaciones para todos los cursos")
    print("2. Generar evaluación para un curso específico")
    print("3. Generar evaluación por categoría")
    print("4. Generar evaluación rápida")
    print("5. Generar todo automáticamente")
    
    # Ejecutar opciones predefinidas
    print("\n🚀 Ejecutando generación automática...")
    
    # Opción 1: Generar para todos los cursos
    generador.generar_evaluaciones_para_todos_cursos(preguntas_por_curso=5)
    
    # Opción 2: Generar evaluación rápida
    generador.generar_evaluacion_rapida(num_preguntas=10)
    
    print("\n" + "="*60)
    print("🎉 ¡GENERACIÓN DE EVALUACIONES COMPLETADA!")
    print("="*60)

if __name__ == "__main__":
    main()
