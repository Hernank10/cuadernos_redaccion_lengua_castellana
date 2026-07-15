#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import glob
import re
from pathlib import Path

# Conectar a SQLite
conn = sqlite3.connect('tecnicas_lengua.db')
cursor = conn.cursor()

# Crear tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS tecnicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    contenido TEXT,
    categoria TEXT,
    subcategoria TEXT,
    grado TEXT,
    tipo TEXT,
    ruta_archivo TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    descripcion TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tecnicas_json (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tecnica_id INTEGER,
    tecnica_numero INTEGER,
    titulo_tecnica TEXT,
    teoria TEXT,
    ejemplo TEXT,
    ejercicio TEXT,
    respuesta TEXT,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE
)
''')

print("✅ Tablas creadas")

# Función para detectar categoría
def detectar_categoria(nombre):
    nombre = nombre.lower()
    if 'gramática' in nombre or 'gramatica' in nombre or 'sintaxis' in nombre or 'morfología' in nombre or 'morfologia' in nombre:
        return 'Gramática y Sintaxis'
    elif 'ortografía' in nombre or 'ortografia' in nombre or 'puntuación' in nombre or 'puntuacion' in nombre:
        return 'Ortografía'
    elif 'literatura' in nombre or 'narrativa' in nombre:
        return 'Literatura y Narrativa'
    elif 'retórica' in nombre or 'retorica' in nombre or 'figura' in nombre:
        return 'Retórica y Figuras'
    elif 'inglés' in nombre or 'ingles' in nombre or 'english' in nombre or 'bilingüe' in nombre or 'bilingue' in nombre:
        return 'Inglés Bilingüe'
    elif 'ciencia ficción' in nombre or 'ciencia ficcion' in nombre or 'ficción' in nombre:
        return 'Ciencia Ficción'
    elif 'men' in nombre or 'saber pro' in nombre or 'saber-pro' in nombre or 'colombia' in nombre:
        return 'Educación Colombia'
    elif 'comprensión' in nombre or 'comprension' in nombre or 'lectura' in nombre:
        return 'Comprensión Lectora'
    elif 'científica' in nombre or 'cientifica' in nombre or 'science' in nombre:
        return 'Redacción Científica'
    elif 'json' in nombre:
        return 'JSON'
    elif 'cuaderno' in nombre:
        return 'Cuadernos'
    else:
        return 'General'

# Función para detectar grado
def detectar_grado(nombre):
    if re.search(r'[1-9]°\s*grado|[1-9][0-9]?\°?\s*grado', nombre):
        return 'Escolar'
    elif 'universitario' in nombre or 'preuniversitario' in nombre:
        return 'Universitario'
    elif 'A1' in nombre or 'A2' in nombre or 'B1' in nombre or 'B2' in nombre or 'C1' in nombre or 'C2' in nombre:
        return 'Nivel Idiomático'
    else:
        return 'General'

# Procesar archivos
ruta_base = '.'
archivos_html = glob.glob(os.path.join(ruta_base, '**', '*.html'), recursive=True)
archivos_json = glob.glob(os.path.join(ruta_base, '**', '*.json'), recursive=True)
archivos_md = glob.glob(os.path.join(ruta_base, '**', '*.md'), recursive=True)
archivos_txt = glob.glob(os.path.join(ruta_base, '**', '*.txt'), recursive=True)
archivos = archivos_html + archivos_json + archivos_md + archivos_txt

print(f"📁 Encontrados {len(archivos)} archivos para procesar")

contador = 0
for archivo in archivos:
    nombre = os.path.basename(archivo)
    categoria = detectar_categoria(nombre)
    grado = detectar_grado(nombre)
    tipo = os.path.splitext(nombre)[1][1:] if '.' in nombre else 'sin_ext'
    
    try:
        # Leer contenido
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            # Limitar tamaño
            if len(contenido) > 100000:
                contenido = contenido[:100000] + '...'
    except:
        contenido = ''
    
    # Insertar
    cursor.execute('''
    INSERT INTO tecnicas (titulo, contenido, categoria, subcategoria, grado, tipo, ruta_archivo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, contenido, categoria, 'general', grado, tipo, archivo))
    
    contador += 1
    if contador % 10 == 0:
        print(f"📄 Procesados {contador} archivos...")

conn.commit()
print(f"✅ Procesados {contador} archivos en total")

# Estadísticas
cursor.execute("SELECT categoria, COUNT(*) FROM tecnicas GROUP BY categoria ORDER BY COUNT(*) DESC")
stats = cursor.fetchall()

print("\n" + "="*50)
print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
print("="*50)
for cat, count in stats:
    print(f"   {cat}: {count} archivos")

print(f"\n📚 Base de datos guardada en: tecnicas_lengua.db")

# Mostrar algunos ejemplos
print("\n📝 Ejemplos de técnicas guardadas:")
cursor.execute("SELECT id, titulo, categoria FROM tecnicas LIMIT 10")
ejemplos = cursor.fetchall()
for id, titulo, categoria in ejemplos:
    print(f"   {id}. [{categoria}] {titulo[:60]}...")

conn.close()
print("\n✅ ¡PROCESO COMPLETADO!")
