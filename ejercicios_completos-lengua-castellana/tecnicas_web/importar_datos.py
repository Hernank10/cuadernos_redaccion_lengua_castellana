#!/usr/bin/env python3
import os
import sys
import sqlite3
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica

print("📥 Importando datos a Django...")

# Conectar a la base de datos SQLite original
conn = sqlite3.connect('tecnicas_lengua.db')
cursor = conn.cursor()

# Verificar si la tabla existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tecnicas'")
if not cursor.fetchone():
    print("❌ La tabla 'tecnicas' no existe en la base de datos")
    print("📋 Tablas disponibles:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")
    conn.close()
    sys.exit(1)

# Obtener datos
cursor.execute("SELECT id, titulo, contenido, categoria, subcategoria, grado, tipo, ruta_archivo FROM tecnicas")
rows = cursor.fetchall()

print(f"📊 Encontradas {len(rows)} técnicas en la base de datos SQLite")

contador = 0
for row in rows:
    id, titulo, contenido, categoria, subcategoria, grado, tipo, ruta = row
    
    tecnica, created = Tecnica.objects.get_or_create(
        id=id,
        defaults={
            'titulo': titulo,
            'contenido': contenido,
            'categoria': categoria or 'General',
            'subcategoria': subcategoria or '',
            'grado': grado or '',
            'tipo': tipo or '',
            'ruta_archivo': ruta or ''
        }
    )
    if created:
        contador += 1
        if contador % 10 == 0:
            print(f"   Importadas {contador} técnicas...")

conn.close()

print(f"✅ Importadas {contador} técnicas nuevas")
print(f"📚 Total en la base de datos: {Tecnica.objects.count()}")
print("🎉 ¡Importación completada!")
