#!/usr/bin/env python3
"""
GENERADOR AUTOMÁTICO DE CURSOS CON SQLITE
- 20 cursos
- Todas las técnicas disponibles
- 100 lecciones por curso
- 10 evaluaciones por curso
"""

import os
import sys
import random
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Tecnica
from cursos.models import Curso, Leccion, Inscripcion
from evaluaciones.models import Evaluacion, Pregunta
from usuarios.models import Usuario

User = get_user_model()

print("="*70)
print("🎓 GENERADOR AUTOMÁTICO DE CURSOS")
print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*70)

# Obtener admin
admin = User.objects.filter(is_superuser=True).first()
if not admin:
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin123'
    )
    print("✅ Superusuario admin creado")

# Obtener técnicas
tecnicas = list(Tecnica.objects.all())
print(f"📚 Técnicas disponibles: {len(tecnicas)}")

if not tecnicas:
    print("❌ No hay técnicas. Importa técnicas primero: python importar_datos.py")
    sys.exit(1)

# Temáticas de cursos
tematicas = [
    {"nombre": "Redacción Básica", "nivel": "principiante", "desc": "Fundamentos de redacción en español"},
    {"nombre": "Gramática Avanzada", "nivel": "intermedio", "desc": "Gramática profunda del castellano"},
    {"nombre": "Ortografía Profesional", "nivel": "intermedio", "desc": "Reglas ortográficas avanzadas"},
    {"nombre": "Redacción Científica", "nivel": "avanzado", "desc": "Escritura de artículos científicos"},
    {"nombre": "Literatura Hispanoamericana", "nivel": "intermedio", "desc": "Análisis literario"},
    {"nombre": "Retórica y Argumentación", "nivel": "avanzado", "desc": "Técnicas de persuasión"},
    {"nombre": "Sintaxis del Español", "nivel": "intermedio", "desc": "Estructura de oraciones"},
    {"nombre": "Comprensión Lectora", "nivel": "principiante", "desc": "Estrategias de lectura"},
    {"nombre": "Escritura Creativa", "nivel": "intermedio", "desc": "Técnicas de narrativa"},
    {"nombre": "Lingüística Aplicada", "nivel": "avanzado", "desc": "Lingüística y enseñanza"},
    {"nombre": "Fonética y Fonología", "nivel": "intermedio", "desc": "Sonidos del español"},
    {"nombre": "Semántica y Pragmática", "nivel": "avanzado", "desc": "Significado y contexto"},
    {"nombre": "Historia de la Lengua", "nivel": "intermedio", "desc": "Evolución del castellano"},
    {"nombre": "Didáctica de la Lengua", "nivel": "avanzado", "desc": "Enseñanza del español"},
    {"nombre": "Análisis del Discurso", "nivel": "avanzado", "desc": "Discurso y comunicación"},
    {"nombre": "Lexicografía", "nivel": "intermedio", "desc": "Estudio del vocabulario"},
    {"nombre": "Normativa y Uso", "nivel": "intermedio", "desc": "Normas de la RAE"},
    {"nombre": "Comunicación Escrita", "nivel": "principiante", "desc": "Comunicación efectiva"},
    {"nombre": "Géneros Literarios", "nivel": "intermedio", "desc": "Tipos de literatura"},
    {"nombre": "Investigación Lingüística", "nivel": "avanzado", "desc": "Métodos de investigación"},
]

cursos_creados = 0
lecciones_creadas = 0
evaluaciones_creadas = 0
preguntas_creadas = 0

print("\n🚀 CREANDO CURSOS...")
print("-"*70)

for i, tematica in enumerate(tematicas[:20]):
    print(f"\n📝 Curso {i+1}/20: {tematica['nombre']}")
    
    # Crear curso
    curso, creado = Curso.objects.get_or_create(
        titulo=tematica['nombre'],
        defaults={
            'descripcion': tematica['desc'],
            'nivel': tematica['nivel'],
            'duracion_horas': random.randint(20, 60),
            'publicado': True,
            'creador': admin
        }
    )
    
    if creado:
        cursos_creados += 1
        
        # Asignar técnicas (30 por curso)
        tecnicas_curso = random.sample(tecnicas, min(30, len(tecnicas)))
        curso.tecnicas.add(*tecnicas_curso)
        print(f"  ✅ Curso creado con {len(tecnicas_curso)} técnicas")
        
        # Crear 100 lecciones
        lec_count = 0
        for j in range(100):
            tecnica = random.choice(tecnicas_curso)
            leccion, c = Leccion.objects.get_or_create(
                curso=curso,
                titulo=f"Lección {j+1}: {tecnica.titulo[:35]}",
                defaults={
                    'descripcion': f"Lección {j+1} del curso {curso.titulo}",
                    'tecnica': tecnica,
                    'orden': j + 1,
                    'duracion_minutos': random.randint(5, 15)
                }
            )
            if c:
                lec_count += 1
                lecciones_creadas += 1
        
        print(f"  📖 {lec_count} lecciones creadas")
        
        # Crear 10 evaluaciones
        eval_count = 0
        tipos_eval = ['diagnostico', 'formativa', 'sumativa', 'final']
        
        for k in range(10):
            tipo = random.choice(tipos_eval)
            num_preg = random.randint(5, 12)
            
            evaluacion, c = Evaluacion.objects.get_or_create(
                curso=curso,
                titulo=f"Evaluación {k+1}: {tematica['nombre'][:20]}",
                defaults={
                    'descripcion': f"Evaluación {k+1} del curso {tematica['nombre']}",
                    'tipo': tipo,
                    'duracion_minutos': num_preg * 2 + 5,
                    'puntaje_maximo': num_preg * 10,
                    'publicado': True
                }
            )
            
            if c:
                eval_count += 1
                evaluaciones_creadas += 1
                
                # Crear preguntas
                preg_count = 0
                for l in range(num_preg):
                    pregunta, pc = Pregunta.objects.get_or_create(
                        evaluacion=evaluacion,
                        pregunta=f"Pregunta {l+1}: ¿Qué sabes sobre {tematica['nombre'][:20]}?",
                        defaults={
                            'tipo': random.choice(['multiple', 'verdadero_falso', 'completar']),
                            'opciones': ['Opción A', 'Opción B', 'Opción C', 'Opción D'],
                            'respuesta_correcta': '0',
                            'puntaje': random.randint(5, 10),
                            'orden': l + 1
                        }
                    )
                    if pc:
                        preg_count += 1
                        preguntas_creadas += 1
                
                print(f"  📝 Evaluación {k+1}: {preg_count} preguntas")
        
        print(f"  ✅ {eval_count} evaluaciones creadas")
    else:
        print(f"  ℹ️ Curso ya existe")

print("\n" + "="*70)
print("📊 RESUMEN FINAL")
print(f"  📚 Cursos creados: {cursos_creados}")
print(f"  📖 Lecciones creadas: {lecciones_creadas}")
print(f"  📝 Evaluaciones creadas: {evaluaciones_creadas}")
print(f"  ❓ Preguntas creadas: {preguntas_creadas}")
print("="*70)

print("\n🌐 Accede al sistema:")
print("  http://localhost:8000/admin/")
print("  http://localhost:8000/cursos/")
