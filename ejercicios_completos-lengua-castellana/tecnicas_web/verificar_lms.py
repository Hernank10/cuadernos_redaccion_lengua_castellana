#!/usr/bin/env python3
"""
Script de verificación completa del LMS
Ejecutar con: python manage.py shell < verificar_lms.py
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')

import django
django.setup()

from core.models import Tecnica
from usuarios.models import Usuario
from cursos.models import Curso, Inscripcion, Certificado, Insignia
from evaluaciones.models import Evaluacion, Pregunta

print("=" * 60)
print("🔍 VERIFICACIÓN COMPLETA DEL LMS")
print("=" * 60)

# 1. Datos principales
print("\n📊 DATOS PRINCIPALES:")
print(f"  👤 Usuarios: {Usuario.objects.count()}")
print(f"  📚 Técnicas: {Tecnica.objects.count()}")
print(f"  📖 Cursos: {Curso.objects.count()}")
print(f"  📝 Inscripciones: {Inscripcion.objects.count()}")
print(f"  📋 Evaluaciones: {Evaluacion.objects.count()}")
print(f"  ❓ Preguntas: {Pregunta.objects.count()}")
print(f"  🏆 Insignias: {Insignia.objects.count()}")
print(f"  🎓 Certificados: {Certificado.objects.count()}")

# 2. Categorías de técnicas
print("\n📚 TÉCNICAS POR CATEGORÍA (Top 5):")
from django.db import models
categorias = Tecnica.objects.values('categoria').annotate(
    count=models.Count('id')
).order_by('-count')[:5]
for cat in categorias:
    print(f"  {cat['categoria']}: {cat['count']}")

# 3. Evaluaciones públicas
print("\n📋 EVALUACIONES PÚBLICAS:")
evaluaciones = Evaluacion.objects.filter(publicado=True)
if evaluaciones:
    for e in evaluaciones[:3]:
        print(f"  ✅ {e.titulo[:40]}... - {e.preguntas.count()} preguntas")
else:
    print("  ⚠️ No hay evaluaciones públicas")

# 4. Certificados
print("\n🎓 CERTIFICADOS:")
certificados = Certificado.objects.all()
if certificados:
    print(f"  ✅ {certificados.count()} certificados generados")
else:
    print("  ⚠️ No hay certificados")

# 5. Cursos con inscripciones
print("\n📖 CURSOS CON INSCRIPCIONES:")
cursos = Curso.objects.filter(publicado=True)
for c in cursos[:5]:
    count = Inscripcion.objects.filter(curso=c).count()
    print(f"  {c.titulo[:35]}... - {count} inscritos")

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 60)
