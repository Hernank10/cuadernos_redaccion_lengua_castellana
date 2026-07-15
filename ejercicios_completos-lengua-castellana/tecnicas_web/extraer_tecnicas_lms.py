#!/usr/bin/env python3
import os
import sys
import json
import re
import django
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Tecnica
from cursos.models import Curso, Leccion

User = get_user_model()

print("🚀 ESTRUCTURANDO LMS CON TÉCNICAS INDIVIDUALES")

# 1. Obtener o crear un usuario administrador
def obtener_admin():
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("👤 Creando superusuario admin...")
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin123'
        )
        print("✅ Superusuario admin creado (admin/admin123)")
    else:
        print(f"👤 Usando superusuario: {admin.username}")
    return admin

admin_user = obtener_admin()

# 2. Crear o obtener el curso principal
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
    print(f"📚 Usando curso existente: {curso.titulo}")

# 3. Función para extraer técnicas del HTML
def extraer_tecnicas_del_html(contenido_html):
    tecnicas = []
    
    if not contenido_html:
        return tecnicas
    
    # Buscar JSON en el HTML
    patron_json = r'```json\s*(\{.*?\})\s*```|```\s*(\{.*?\})\s*```|(\{.*?"técnicas".*?\})'
    matches = re.findall(patron_json, contenido_html, re.DOTALL)
    
    for match in matches:
        for grupo in match:
            if grupo and len(grupo) > 50:
                try:
                    datos = json.loads(grupo)
                    if isinstance(datos, dict):
                        for key in ['técnicas', 'tecnicas', 'items', 'data']:
                            if key in datos and isinstance(datos[key], list):
                                for item in datos[key]:
                                    if isinstance(item, dict):
                                        tecnicas.append({
                                            'titulo': item.get('titulo', f'Técnica {len(tecnicas)+1}'),
                                            'teoria': item.get('teoria', ''),
                                            'ejemplo': item.get('ejemplo', ''),
                                            'ejercicio': item.get('ejercicio', ''),
                                            'respuesta': item.get('respuesta', '')
                                        })
                                break
                except:
                    pass
    
    # Si no se encontró JSON, buscar con BeautifulSoup
    if not tecnicas and len(contenido_html) > 100:
        try:
            soup = BeautifulSoup(contenido_html, 'html.parser')
            elementos = soup.find_all(['div', 'section', 'article'], 
                                       class_=re.compile(r'(tecnica|card|flashcard|ejercicio)', re.I))
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
                        'respuesta': ''
                    })
        except:
            pass
    
    return tecnicas

# 4. Procesar todas las técnicas
tecnicas_django = Tecnica.objects.all()
total_tecnicas_procesadas = 0
total_lecciones_creadas = 0

print(f"\n📊 Procesando {tecnicas_django.count()} archivos HTML...")
print("=" * 50)

for idx, tecnica in enumerate(tecnicas_django):
    if not tecnica.contenido:
        continue
    
    # Extraer técnicas internas
    tecnicas_internas = extraer_tecnicas_del_html(tecnica.contenido)
    
    if tecnicas_internas:
        total_tecnicas_procesadas += 1
        print(f"📄 {idx+1}/{tecnicas_django.count()}: {tecnica.titulo[:40]}... → {len(tecnicas_internas)} técnicas")
        
        # Crear lecciones para cada técnica interna
        for i, tech in enumerate(tecnicas_internas[:100]):
            titulo = tech.get('titulo', f'Técnica {i+1}')[:100]
            descripcion = tech.get('teoria', '')[:500]
            
            if tech.get('ejemplo'):
                descripcion += f"\n\nEjemplo: {tech['ejemplo'][:200]}"
            
            # Verificar si la lección ya existe
            leccion, creada = Leccion.objects.get_or_create(
                curso=curso,
                titulo=titulo,
                defaults={
                    'descripcion': descripcion,
                    'tecnica': tecnica,
                    'orden': total_lecciones_creadas + i + 1,
                    'duracion_minutos': 5
                }
            )
            if creada:
                total_lecciones_creadas += 1
        
        # Asociar el archivo original al curso
        curso.tecnicas.add(tecnica)

print("=" * 50)
print(f"\n📊 ESTADÍSTICAS DEL LMS:")
print(f"   📚 Curso: {curso.titulo}")
print(f"   👤 Creador: {admin_user.username}")
print(f"   📝 Archivos HTML procesados: {total_tecnicas_procesadas}")
print(f"   📖 Lecciones creadas: {total_lecciones_creadas}")
print(f"   🎯 Técnicas en curso: {curso.tecnicas.count()}")
print(f"   📈 Total de recursos: {curso.tecnicas.count() + total_lecciones_creadas}")

print("\n✅ LMS estructurado exitosamente!")
