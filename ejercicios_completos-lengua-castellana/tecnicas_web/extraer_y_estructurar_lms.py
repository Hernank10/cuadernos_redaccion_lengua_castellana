#!/usr/bin/env python3
import os
import sys
import json
import re
import django
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica
from cursos.models import Curso, Leccion
from usuarios.models import Usuario

print("🚀 ESTRUCTURANDO LMS CON TÉCNICAS INDIVIDUALES")

def extraer_tecnicas_del_html(contenido_html, titulo_archivo):
    """Extrae técnicas individuales del HTML"""
    tecnicas = []
    
    # Buscar JSON en el HTML
    patron_json = r'```json\s*(\{.*?\})\s*```|```\s*(\{.*?\})\s*```|(\{.*?"técnicas".*?\})'
    matches = re.findall(patron_json, contenido_html, re.DOTALL)
    
    for match in matches:
        for grupo in match:
            if grupo and len(grupo) > 50:
                try:
                    datos = json.loads(grupo)
                    if isinstance(datos, dict):
                        # Buscar lista de técnicas
                        for key in ['técnicas', 'tecnicas', 'items', 'data', 'contenido']:
                            if key in datos and isinstance(datos[key], list):
                                for item in datos[key]:
                                    if isinstance(item, dict):
                                        tecnicas.append({
                                            'titulo': item.get('titulo', f'Técnica {len(tecnicas)+1}'),
                                            'teoria': item.get('teoria', ''),
                                            'ejemplo': item.get('ejemplo', ''),
                                            'ejercicio': item.get('ejercicio', ''),
                                            'respuesta': item.get('respuesta', ''),
                                            'categoria': 'General'
                                        })
                                break
                except:
                    pass
    
    # Si no se encontró JSON, buscar con BeautifulSoup
    if not tecnicas:
        soup = BeautifulSoup(contenido_html, 'html.parser')
        # Buscar elementos de flashcard o ejercicio
        elementos = soup.find_all(['div', 'section', 'article'], 
                                   class_=re.compile(r'(tecnica|card|flashcard|ejercicio|pregunta)', re.I))
        for elem in elementos[:100]:
            texto = elem.get_text(strip=True)
            if texto and len(texto) > 20:
                titulo_elem = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'strong'])
                titulo = titulo_elem.get_text(strip=True) if titulo_elem else f'Técnica {len(tecnicas)+1}'
                tecnicas.append({
                    'titulo': titulo[:200],
                    'teoria': texto[:500],
                    'ejemplo': '',
                    'ejercicio': '',
                    'respuesta': '',
                    'categoria': 'General'
                })
    
    return tecnicas

# Obtener o crear un usuario administrador para ser el creador
try:
    admin_user = Usuario.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("⚠️ No hay superusuario. Creando uno...")
        admin_user = Usuario.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin123'
        )
        print(f"✅ Superusuario admin creado")
except:
    print("❌ Error al crear superusuario")
    sys.exit(1)

print(f"👤 Usando usuario: {admin_user.username} (ID: {admin_user.id})")

# Crear curso principal con el creador
curso, creado = Curso.objects.get_or_create(
    titulo="Técnicas de Lengua Castellana - Curso Completo",
    defaults={
        'descripcion': "Curso completo de técnicas de lengua castellana con más de 300 recursos interactivos",
        'nivel': 'principiante',
        'duracion_horas': 50,
        'publicado': True,
        'creador': admin_user
    }
)

if creado:
    print(f"✅ Curso creado: {curso.titulo}")
else:
    print(f"📚 Curso existente: {curso.titulo}")

# Procesar todas las técnicas
tecnicas_django = Tecnica.objects.all()
total_tecnicas_extraidas = 0
total_lecciones_creadas = 0
tecnica_individual_count = 0

print(f"\n📊 Procesando {tecnicas_django.count()} archivos HTML...")

for idx, tecnica in enumerate(tecnicas_django):
    if not tecnica.contenido:
        continue
    
    print(f"📄 Procesando {idx+1}/{tecnicas_django.count()}: {tecnica.titulo[:50]}...")
    
    # Extraer técnicas internas
    tecnicas_internas = extraer_tecnicas_del_html(tecnica.contenido, tecnica.titulo)
    
    if tecnicas_internas:
        # Crear lecciones para cada técnica interna
        for i, tech in enumerate(tecnicas_internas[:100]):  # Limitar a 100 por módulo
            leccion_titulo = tech.get('titulo', f'Técnica {i+1}')[:100]
            
            # Verificar si la lección ya existe
            leccion, creada = Leccion.objects.get_or_create(
                curso=curso,
                titulo=leccion_titulo,
                defaults={
                    'descripcion': tech.get('teoria', '')[:500],
                    'tecnica': tecnica,
                    'orden': len(tecnicas_internas) * 100 + i + 1,
                    'duracion_minutos': 5
                }
            )
            if creada:
                total_lecciones_creadas += 1
                tecnica_individual_count += 1
                
                # Si tiene ejemplo, agregarlo a la descripción
                if tech.get('ejemplo'):
                    leccion.descripcion += f"\n\nEjemplo: {tech['ejemplo'][:200]}"
                    leccion.save()
        
        total_tecnicas_extraidas += len(tecnicas_internas)
        
        # Asociar el archivo original al curso
        curso.tecnicas.add(tecnica)

# Estadísticas
print(f"\n📊 ESTADÍSTICAS DEL LMS:")
print(f"   📚 Curso: {curso.titulo}")
print(f"   👤 Creador: {admin_user.username}")
print(f"   📝 Archivos HTML en el curso: {curso.tecnicas.count()}")
print(f"   📖 Lecciones creadas: {total_lecciones_creadas}")
print(f"   🎯 Técnicas individuales extraídas: {tecnica_individual_count}")
print(f"   📈 Total de recursos: {curso.tecnicas.count() + total_lecciones_creadas}")

print("\n✅ LMS estructurado exitosamente!")
