#!/usr/bin/env python3
import os
import sys
import json
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Tecnica
from cursos.models import Curso, Leccion

User = get_user_model()

print("🚀 EXTRAYENDO TÉCNICAS PARA LMS")
print("=" * 60)

# Obtener admin
admin = User.objects.filter(is_superuser=True).first()
if not admin:
    print("👤 Creando superusuario admin...")
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin123'
    )
    print("✅ Superusuario creado (admin/admin123)")
else:
    print(f"✅ Usando superusuario: {admin.username}")

# Crear o obtener curso
curso, creado = Curso.objects.get_or_create(
    titulo='Técnicas de Lengua Castellana - Curso Completo',
    defaults={
        'descripcion': 'Curso completo con todas las técnicas de lengua castellana para estudiantes y profesionales',
        'nivel': 'principiante',
        'duracion_horas': 50,
        'publicado': True,
        'creador': admin
    }
)

if creado:
    print(f"✅ Curso creado: {curso.titulo}")
else:
    print(f"📚 Usando curso existente: {curso.titulo}")

# Procesar técnicas
tecnicas = Tecnica.objects.all()
print(f"\n📊 Procesando {tecnicas.count()} archivos HTML...")
print("-" * 60)

total_lecciones = 0
archivos_procesados = 0

for i, tecnica in enumerate(tecnicas):
    if not tecnica.contenido:
        continue
    
    contenido = tecnica.contenido
    tecnicas_internas = []
    
    # Buscar JSON en el contenido
    patrones = [
        r'```json\s*(\{.*?\})\s*```',
        r'```\s*(\{.*?\})\s*```',
        r'(\{.*?"técnicas".*?\})',
        r'(\{.*?"tecnicas".*?\})'
    ]
    
    for patron in patrones:
        matches = re.findall(patron, contenido, re.DOTALL)
        for match in matches:
            try:
                datos = json.loads(match)
                if isinstance(datos, dict):
                    for key in ['técnicas', 'tecnicas', 'items', 'data']:
                        if key in datos and isinstance(datos[key], list):
                            for item in datos[key]:
                                if isinstance(item, dict):
                                    tecnicas_internas.append({
                                        'titulo': item.get('titulo', f'Técnica {len(tecnicas_internas)+1}'),
                                        'descripcion': item.get('teoria', item.get('descripcion', ''))[:300]
                                    })
                            break
            except:
                pass
        
        if tecnicas_internas:
            break
    
    if tecnicas_internas:
        archivos_procesados += 1
        print(f"📄 {i+1}/{tecnicas.count()}: {tecnica.titulo[:45]}... → {len(tecnicas_internas)} técnicas")
        
        # Crear lecciones
        for j, tech in enumerate(tecnicas_internas[:100]):
            titulo = tech.get('titulo', f'Técnica {j+1}')[:100]
            
            leccion, creada = Leccion.objects.get_or_create(
                curso=curso,
                titulo=titulo,
                defaults={
                    'descripcion': tech.get('descripcion', '')[:500],
                    'tecnica': tecnica,
                    'orden': total_lecciones + j + 1,
                    'duracion_minutos': 5
                }
            )
            if creada:
                total_lecciones += 1

print("-" * 60)
print("\n📊 ESTADÍSTICAS FINALES:")
print(f"   📚 Curso: {curso.titulo}")
print(f"   📝 Archivos HTML procesados: {archivos_procesados}")
print(f"   📖 Lecciones creadas: {total_lecciones}")
print(f"   🎯 Total técnicas en base: {Tecnica.objects.count()}")
print(f"   📈 Total recursos en curso: {curso.tecnicas.count() + total_lecciones}")

print("\n✅ ¡LMS estructurado exitosamente!")
