#!/usr/bin/env python3
import os
import sys
import sqlite3
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica

print("📥 Importando datos...")

conn = sqlite3.connect('tecnicas_lengua.db')
cursor = conn.cursor()

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
            'categoria': categoria,
            'subcategoria': subcategoria,
            'grado': grado,
            'tipo': tipo,
            'ruta_archivo': ruta
        }
    )
    if created:
        contador += 1

conn.close()

print(f"✅ Importadas {contador} técnicas nuevas")
print(f"📚 Total en la base de datos: {Tecnica.objects.count()}")
print("🎉 ¡Importación completada!")
