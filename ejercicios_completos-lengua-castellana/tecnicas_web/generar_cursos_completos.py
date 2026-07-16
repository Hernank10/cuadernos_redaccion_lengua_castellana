#!/usr/bin/env python3
"""
GENERADOR AUTOMÁTICO DE CURSOS COMPLETOS
- 20 cursos
- 306 técnicas organizadas
- 100 lecciones por curso
- 10 evaluaciones por curso
- MySQL integrado
"""

import os
import sys
import random
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Tecnica
from cursos.models import Curso, Leccion, Inscripcion
from evaluaciones.models import Evaluacion, Pregunta
from usuarios.models import Usuario

User = get_user_model()

class GeneradorCursosAutomatico:
    """Generador automático de cursos completos"""
    
    def __init__(self):
        self.admin = User.objects.filter(is_superuser=True).first()
        if not self.admin:
            self.admin = User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='admin123'
            )
            print("✅ Superusuario admin creado")
        
        self.tecnicas = list(Tecnica.objects.all())
        self.cursos_creados = 0
        self.lecciones_creadas = 0
        self.evaluaciones_creadas = 0
        self.preguntas_creadas = 0
        
        # Temáticas de cursos
        self.tematicas = [
            {"nombre": "Redacción Básica", "nivel": "principiante", "descripcion": "Fundamentos de redacción en español"},
            {"nombre": "Gramática Avanzada", "nivel": "intermedio", "descripcion": "Gramática profunda del castellano"},
            {"nombre": "Ortografía Profesional", "nivel": "intermedio", "descripcion": "Reglas ortográficas avanzadas"},
            {"nombre": "Redacción Científica", "nivel": "avanzado", "descripcion": "Escritura de artículos científicos"},
            {"nombre": "Literatura Hispanoamericana", "nivel": "intermedio", "descripcion": "Análisis literario"},
            {"nombre": "Retórica y Argumentación", "nivel": "avanzado", "descripcion": "Técnicas de persuasión"},
            {"nombre": "Sintaxis del Español", "nivel": "intermedio", "descripcion": "Estructura de oraciones"},
            {"nombre": "Comprensión Lectora", "nivel": "principiante", "descripcion": "Estrategias de lectura"},
            {"nombre": "Escritura Creativa", "nivel": "intermedio", "descripcion": "Técnicas de narrativa"},
            {"nombre": "Lingüística Aplicada", "nivel": "avanzado", "descripcion": "Lingüística y enseñanza"},
            {"nombre": "Fonética y Fonología", "nivel": "intermedio", "descripcion": "Sonidos del español"},
            {"nombre": "Semántica y Pragmática", "nivel": "avanzado", "descripcion": "Significado y contexto"},
            {"nombre": "Historia de la Lengua", "nivel": "intermedio", "descripcion": "Evolución del castellano"},
            {"nombre": "Didáctica de la Lengua", "nivel": "avanzado", "descripcion": "Enseñanza del español"},
            {"nombre": "Análisis del Discurso", "nivel": "avanzado", "descripcion": "Discurso y comunicación"},
            {"nombre": "Lexicografía", "nivel": "intermedio", "descripcion": "Estudio del vocabulario"},
            {"nombre": "Normativa y Uso", "nivel": "intermedio", "descripcion": "Normas de la RAE"},
            {"nombre": "Comunicación Escrita", "nivel": "principiante", "descripcion": "Comunicación efectiva"},
            {"nombre": "Géneros Literarios", "nivel": "intermedio", "descripcion": "Tipos de literatura"},
            {"nombre": "Investigación Lingüística", "nivel": "avanzado", "descripcion": "Métodos de investigación"},
        ]
        
        # Tipos de preguntas para evaluaciones
        self.tipos_preguntas = ['multiple', 'verdadero_falso', 'completar', 'abierta']
    
    def crear_cursos(self):
        """Crea 20 cursos con diferentes temáticas"""
        print("\n" + "="*70)
        print("🚀 GENERANDO 20 CURSOS AUTOMÁTICAMENTE")
        print("="*70)
        
        if not self.tecnicas:
            print("❌ No hay técnicas disponibles")
            return
        
        print(f"📚 Técnicas disponibles: {len(self.tecnicas)}")
        print(f"👤 Admin: {self.admin.username}")
        print("")
        
        for i, tematica in enumerate(self.tematicas[:20]):
            print(f"📝 Creando curso {i+1}/20: {tematica['nombre']}")
            
            # Crear curso
            curso, creado = Curso.objects.get_or_create(
                titulo=tematica['nombre'],
                defaults={
                    'descripcion': tematica['descripcion'],
                    'nivel': tematica['nivel'],
                    'duracion_horas': random.randint(20, 60),
                    'publicado': True,
                    'creador': self.admin
                }
            )
            
            if creado:
                self.cursos_creados += 1
                print(f"  ✅ Curso creado: {curso.titulo}")
                
                # Asignar técnicas (30 por curso)
                tecnicas_curso = random.sample(self.tecnicas, min(30, len(self.tecnicas)))
                curso.tecnicas.add(*tecnicas_curso)
                print(f"  📚 {len(tecnicas_curso)} técnicas asignadas")
                
                # Crear lecciones (100 por curso)
                lecciones_creadas = self.crear_lecciones(curso, tecnicas_curso)
                print(f"  📖 {lecciones_creadas} lecciones creadas")
                
                # Crear evaluaciones (10 por curso)
                evaluaciones_creadas = self.crear_evaluaciones(curso, tecnicas_curso)
                print(f"  📝 {evaluaciones_creadas} evaluaciones creadas")
                
            else:
                print(f"  ℹ️ Curso ya existe: {curso.titulo}")
            
            print("")
        
        print("="*70)
        print("📊 RESUMEN FINAL")
        print(f"  📚 Cursos creados: {self.cursos_creados}")
        print(f"  📖 Lecciones creadas: {self.lecciones_creadas}")
        print(f"  📝 Evaluaciones creadas: {self.evaluaciones_creadas}")
        print(f"  ❓ Preguntas creadas: {self.preguntas_creadas}")
        print("="*70)
    
    def crear_lecciones(self, curso, tecnicas_curso):
        """Crea 100 lecciones para un curso"""
        lecciones_count = 0
        
        for i in range(100):
            tecnica = random.choice(tecnicas_curso) if tecnicas_curso else None
            
            leccion, creada = Leccion.objects.get_or_create(
                curso=curso,
                titulo=f"Lección {i+1}: {tecnica.titulo[:30] if tecnica else f'Técnica {i+1}'}",
                defaults={
                    'descripcion': f"Lección {i+1} del curso {curso.titulo}. Basada en: {tecnica.titulo[:100] if tecnica else 'Contenido general'}",
                    'tecnica': tecnica,
                    'orden': i + 1,
                    'duracion_minutos': random.randint(5, 15)
                }
            )
            
            if creada:
                lecciones_count += 1
                self.lecciones_creadas += 1
        
        return lecciones_count
    
    def crear_evaluaciones(self, curso, tecnicas_curso):
        """Crea 10 evaluaciones para un curso"""
        evaluaciones_count = 0
        
        tipos_evaluacion = [
            ('diagnostico', 'Evaluación Diagnóstica'),
            ('formativa', 'Evaluación Formativa'),
            ('sumativa', 'Evaluación Sumativa'),
            ('final', 'Evaluación Final')
        ]
        
        for i in range(10):
            tipo, nombre = random.choice(tipos_evaluacion)
            num_preguntas = random.randint(5, 15)
            
            evaluacion, creada = Evaluacion.objects.get_or_create(
                curso=curso,
                titulo=f"Evaluación {i+1}: {nombre} - {curso.titulo[:20]}",
                defaults={
                    'descripcion': f"Evaluación {i+1} del curso {curso.titulo}. Tipo: {nombre}",
                    'tipo': tipo,
                    'duracion_minutos': num_preguntas * 2 + 5,
                    'puntaje_maximo': num_preguntas * 10,
                    'publicado': True
                }
            )
            
            if creada:
                evaluaciones_count += 1
                self.evaluaciones_creadas += 1
                
                # Crear preguntas
                preguntas_creadas = self.crear_preguntas(evaluacion, tecnicas_curso, num_preguntas)
                self.preguntas_creadas += preguntas_creadas
        
        return evaluaciones_count
    
    def crear_preguntas(self, evaluacion, tecnicas_curso, num_preguntas):
        """Crea preguntas para una evaluación"""
        preguntas_count = 0
        
        for i in range(num_preguntas):
            tipo = random.choice(self.tipos_preguntas)
            tecnica = random.choice(tecnicas_curso) if tecnicas_curso else None
            
            if tipo == 'multiple':
                opciones = [
                    "Opción A: Texto correcto",
                    "Opción B: Texto incorrecto",
                    "Opción C: Otra opción",
                    "Opción D: Última opción"
                ]
                respuesta_correcta = "0"
                texto_pregunta = f"Pregunta {i+1}: ¿Cuál es la opción correcta sobre {tecnica.titulo[:30] if tecnica else 'el tema'}?"
            
            elif tipo == 'verdadero_falso':
                opciones = ["Verdadero", "Falso"]
                respuesta_correcta = random.choice(["V", "F"])
                texto_pregunta = f"Pregunta {i+1}: ¿Es correcta la siguiente afirmación sobre {tecnica.titulo[:30] if tecnica else 'el tema'}?"
            
            elif tipo == 'completar':
                opciones = []
                respuesta_correcta = "palabra correcta"
                texto_pregunta = f"Pregunta {i+1}: Completa la siguiente frase sobre {tecnica.titulo[:30] if tecnica else 'el tema'}: La ________ es importante."
            
            else:  # abierta
                opciones = []
                respuesta_correcta = "Respuesta basada en el contenido"
                texto_pregunta = f"Pregunta {i+1}: Explica con tus palabras el concepto de {tecnica.titulo[:30] if tecnica else 'el tema'}."
            
            pregunta, creada = Pregunta.objects.get_or_create(
                evaluacion=evaluacion,
                pregunta=texto_pregunta,
                defaults={
                    'tipo': tipo,
                    'opciones': opciones,
                    'respuesta_correcta': respuesta_correcta,
                    'puntaje': random.randint(5, 10),
                    'orden': i + 1,
                    'explicacion': f"Explicación de la pregunta {i+1} sobre {tecnica.titulo[:30] if tecnica else 'el tema'}"
                }
            )
            
            if creada:
                preguntas_count += 1
        
        return preguntas_count
    
    def generar_inscripciones_prueba(self):
        """Genera inscripciones de prueba para los cursos"""
        print("\n👤 Generando inscripciones de prueba...")
        
        # Crear estudiantes de prueba
        estudiantes = []
        for i in range(5):
            username = f"estudiante_prueba_{i+1}"
            estudiante, creado = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f"{username}@ejemplo.com",
                    'password': User.objects.make_random_password(),
                    'rol': 'estudiante',
                    'first_name': f"Estudiante",
                    'last_name': f"Prueba {i+1}"
                }
            )
            if creado:
                print(f"  ✅ Estudiante creado: {username}")
            estudiantes.append(estudiante)
        
        # Inscribir estudiantes en cursos
        cursos = Curso.objects.filter(publicado=True)
        for curso in cursos[:10]:  # Los primeros 10 cursos
            for estudiante in estudiantes[:3]:  # 3 estudiantes por curso
                inscripcion, creada = Inscripcion.objects.get_or_create(
                    estudiante=estudiante,
                    curso=curso,
                    defaults={
                        'estado': 'activo',
                        'progreso': random.randint(10, 80),
                        'calificacion': random.randint(60, 95)
                    }
                )
                if creada:
                    print(f"  ✅ {estudiante.username} inscrito en {curso.titulo[:20]}")
        
        print(f"✅ Inscripciones completadas")

def main():
    """Función principal"""
    print("="*70)
    print("🎓 GENERADOR AUTOMÁTICO DE CURSOS COMPLETOS")
    print("📚 LMS - Técnicas de Lengua Castellana")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70)
    
    generador = GeneradorCursosAutomatico()
    
    # Generar cursos
    generador.crear_cursos()
    
    # Generar inscripciones de prueba
    generador.generar_inscripciones_prueba()
    
    print("\n" + "="*70)
    print("🎉 GENERACIÓN COMPLETADA")
    print(f"📊 Total cursos: {Curso.objects.count()}")
    print(f"📖 Total lecciones: {Leccion.objects.count()}")
    print(f"📝 Total evaluaciones: {Evaluacion.objects.count()}")
    print(f"❓ Total preguntas: {Pregunta.objects.count()}")
    print("="*70)
    
    print("\n🌐 Accede al sistema:")
    print("  http://localhost:8000/admin/")
    print("  http://localhost:8000/cursos/")
    print("  http://localhost:8000/evaluaciones/")

if __name__ == "__main__":
    main()
