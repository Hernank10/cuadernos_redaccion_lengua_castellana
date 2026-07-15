#!/usr/bin/env python3
import os
import sqlite3
import glob
import re

print("🔄 Regenerando base de datos desde archivos HTML...")

# Conectar a la base de datos
conn = sqlite3.connect('tecnicas_lengua.db')
cursor = conn.cursor()

# Crear la tabla tecnicas si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS tecnicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    contenido TEXT,
    categoria TEXT,
    subcategoria TEXT,
    grado TEXT,
    tipo TEXT,
    ruta_archivo TEXT
)
''')

# Buscar archivos HTML
archivos = glob.glob('../**/*.html', recursive=True)
print(f"📁 Encontrados {len(archivos)} archivos HTML")

# Insertar datos
for i, archivo in enumerate(archivos):
    nombre = os.path.basename(archivo)
    
    # Determinar categoría desde la carpeta
    carpeta = os.path.basename(os.path.dirname(archivo))
    categoria = carpeta.replace('_', ' ').title()
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()[:10000]  # Limitar tamaño
    except:
        contenido = ''
    
    # Insertar
    cursor.execute('''
    INSERT INTO tecnicas (titulo, contenido, categoria, ruta_archivo)
    VALUES (?, ?, ?, ?)
    ''', (nombre, contenido, categoria, archivo))
    
    if (i + 1) % 10 == 0:
        print(f"   Procesados {i+1} archivos...")

conn.commit()
conn.close()

print(f"✅ Base de datos regenerada con {len(archivos)} técnicas")
