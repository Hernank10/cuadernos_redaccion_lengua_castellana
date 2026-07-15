#!/usr/bin/env python3
import os
import sqlite3
import glob
import re

print("🔄 REGENERANDO BASE DE DATOS CON TODAS LAS TÉCNICAS")
print("="*60)

# Conectar a la base de datos
conn = sqlite3.connect('tecnicas_lengua.db')
cursor = conn.cursor()

# Crear la tabla tecnicas (para importar a Django)
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

# Buscar archivos HTML en el directorio superior
archivos = glob.glob('../**/*.html', recursive=True)
print(f"📁 Encontrados {len(archivos)} archivos HTML")

# Insertar datos
contador = 0
for archivo in archivos:
    nombre = os.path.basename(archivo)
    
    # Determinar categoría desde la carpeta
    carpeta = os.path.basename(os.path.dirname(archivo))
    categoria = carpeta.replace('_', ' ').title()
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()[:50000]  # Limitar tamaño
    except:
        contenido = ''
    
    # Determinar tipo
    tipo = 'html'
    if nombre.endswith('.json'):
        tipo = 'json'
    
    # Insertar
    cursor.execute('''
    INSERT INTO tecnicas (titulo, contenido, categoria, tipo, ruta_archivo)
    VALUES (?, ?, ?, ?, ?)
    ''', (nombre, contenido, categoria, tipo, archivo))
    
    contador += 1
    if contador % 10 == 0:
        print(f"   Procesados {contador} archivos...")

conn.commit()
conn.close()

print(f"✅ Base de datos regenerada con {contador} técnicas")
print("📊 Tablas disponibles:")
os.system("sqlite3 tecnicas_lengua.db '.tables'")
