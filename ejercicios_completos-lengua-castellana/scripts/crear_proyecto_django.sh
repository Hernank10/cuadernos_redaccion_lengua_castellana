#!/bin/bash

echo "🚀 Creando proyecto Django para Técnicas de Lengua Castellana"

# Instalar Django
pip install django django-crispy-forms

# Crear proyecto
django-admin startproject tecnicas_web
cd tecnicas_web

# Crear app core
python3 manage.py startapp core

# Copiar la base de datos existente
cp ../tecnicas_lengua.db .

# Crear estructura de carpetas
mkdir -p core/templates/core
mkdir -p static/css
mkdir -p static/js

echo "✅ Proyecto creado exitosamente"
echo "📁 Directorio: $(pwd)"
