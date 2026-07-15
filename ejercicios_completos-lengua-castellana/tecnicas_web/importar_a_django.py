#!/usr/bin/env python3
import os
import sys
import sqlite3
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica

print("📥 IMPORTANDO TÉCNICAS A DJANGO")
print("="*60)

# Conectar a la base de datos SQLite
conn = sqlite3.connect('tecnicas_lengua.db')
cursor = conn.cursor()

# Verificar si la tabla existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tecnicas'")
if not cursor.fetchone():
    print("❌ La tabla 'tecnicas' no existe")
    conn.close()
    sys.exit(1)

# Obtener datos
cursor.execute("SELECT id, titulo, contenido, categoria, subcategoria, grado, tipo, ruta_archivo FROM tecnicas")
rows = cursor.fetchall()

print(f"📊 Encontradas {len(rows)} técnicas en la base de datos SQLite")

contador = 0
errores = 0

for row in rows:
    try:
        id, titulo, contenido, categoria, subcategoria, grado, tipo, ruta = row
        
        # Manejar valores nulos
        titulo = titulo or f"Técnica {id}"
        categoria = categoria or 'General'
        subcategoria = subcategoria or ''
        grado = grado or ''
        tipo = tipo or 'html'
        ruta_archivo = ruta or ''
        contenido = contenido or ''
        
        # Crear o actualizar
        tecnica, created = Tecnica.objects.get_or_create(
            id=id,
            defaults={
                'titulo': titulo,
                'contenido': contenido,
                'categoria': categoria,
                'subcategoria': subcategoria,
                'grado': grado,
                'tipo': tipo,
                'ruta_archivo': ruta_archivo
            }
        )
        if created:
            contador += 1
            if contador % 10 == 0:
                print(f"   Importadas {contador} técnicas...")
    except Exception as e:
        errores += 1
        print(f"   ⚠️ Error en ID {id}: {str(e)[:50]}")

conn.close()

print(f"\n✅ Importadas {contador} técnicas nuevas")
print(f"⚠️ {errores} errores encontrados")
print(f"📚 Total en la base de datos: {Tecnica.objects.count()}")
print("🎉 ¡Importación completada!")
