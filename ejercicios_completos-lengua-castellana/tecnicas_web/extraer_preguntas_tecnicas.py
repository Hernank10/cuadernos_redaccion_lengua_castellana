#!/usr/bin/env python3
"""
Extractor de Preguntas de Técnicas
Analiza todas las técnicas y extrae preguntas potenciales
"""

import re
import json
import django
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica

print("🔍 EXTRACTOR DE PREGUNTAS DE TÉCNICAS")
print("="*60)

# Palabras clave que indican preguntas
PATRONES_PREGUNTAS = [
    r'\?',  # Signos de interrogación
    r'¿',   # Signos de interrogación españoles
    r'pregunta', r'cuestion', r'ejercicio',
    r'flashcard', r'quiz', r'test',
    r'selecciona', r'elige', r'responde',
    r'completa', r'relaciona', r'ordena'
]

def extraer_preguntas_tecnicas():
    """Extrae preguntas de todas las técnicas"""
    tecnicas = Tecnica.objects.all()
    total_preguntas = 0
    tecnicas_con_preguntas = 0
    
    print(f"📚 Analizando {tecnicas.count()} técnicas...")
    print("-"*60)
    
    for tecnica in tecnicas:
        if not tecnica.contenido:
            continue
        
        contenido = tecnica.contenido
        
        # Buscar patrones de preguntas
        preguntas_encontradas = []
        
        # Buscar en JSON
        patron_json = r'```json\s*(\{.*?\})\s*```'
        matches = re.findall(patron_json, contenido, re.DOTALL)
        
        for match in matches:
            try:
                datos = json.loads(match)
                for key in ['preguntas', 'ejercicios', 'items', 'quiz']:
                    if key in datos and isinstance(datos[key], list):
                        for item in datos[key]:
                            if isinstance(item, dict):
                                texto = item.get('pregunta', item.get('titulo', ''))
                                if texto and len(texto) > 10:
                                    preguntas_encontradas.append(texto)
            except:
                pass
        
        # Buscar líneas con signos de interrogación
        lineas = contenido.split('\n')
        for linea in lineas:
            if '?' in linea or '¿' in linea:
                if len(linea.strip()) > 15:
                    preguntas_encontradas.append(linea.strip())
        
        if preguntas_encontradas:
            tecnicas_con_preguntas += 1
            total_preguntas += len(preguntas_encontradas)
            print(f"✅ {tecnica.titulo[:40]}... → {len(preguntas_encontradas)} preguntas")
    
    print("-"*60)
    print(f"📊 RESULTADOS:")
    print(f"   Técnicas con preguntas: {tecnicas_con_preguntas}")
    print(f"   Total de preguntas: {total_preguntas}")
    print(f"   Promedio por técnica: {total_preguntas/tecnicas_con_preguntas:.1f}" if tecnicas_con_preguntas > 0 else "   N/A")
    print("="*60)

if __name__ == "__main__":
    extraer_preguntas_tecnicas()
