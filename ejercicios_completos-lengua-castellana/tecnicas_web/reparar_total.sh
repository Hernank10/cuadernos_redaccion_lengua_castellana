#!/bin/bash
echo "🔧 REPARACIÓN COMPLETA"

# 1. Verificar archivos necesarios
echo "📁 Verificando archivos..."
[ -f core/urls.py ] && echo "✅ core/urls.py existe" || echo "❌ FALTA core/urls.py"
[ -f core/views.py ] && echo "✅ core/views.py existe" || echo "❌ FALTA core/views.py"
[ -f core/models.py ] && echo "✅ core/models.py existe" || echo "❌ FALTA core/models.py"

# 2. Crear archivos si faltan
if [ ! -f core/urls.py ]; then
    echo "📝 Creando core/urls.py..."
    cat > core/urls.py << 'URLS'
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('tecnicas/', views.tecnicas_list, name='tecnicas_list'),
    path('tecnica/<int:pk>/', views.tecnica_detail, name='tecnica_detail'),
    path('categorias/', views.categorias, name='categorias'),
    path('buscar/', views.buscar, name='buscar'),
]
URLS
fi

# 3. Verificar tecnicas_web/urls.py
if ! grep -q "include('core.urls')" tecnicas_web/urls.py; then
    echo "📝 Actualizando tecnicas_web/urls.py..."
    cat > tecnicas_web/urls.py << 'MAINURLS'
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
MAINURLS
fi

# 4. Limpiar y recrear migraciones
echo "🔄 Limpiando migraciones..."
rm -rf core/migrations/
rm -rf __pycache__

echo "📊 Creando migraciones..."
python3 manage.py makemigrations core
python3 manage.py migrate

# 5. Importar datos
echo "📥 Importando datos..."
python3 importar_datos.py

# 6. Verificar
echo "🔍 Verificando instalación..."
python3 manage.py check

echo "✅ Reparación completada"
echo "🚀 Iniciando servidor..."
python3 manage.py runserver 0.0.0.0:8000
