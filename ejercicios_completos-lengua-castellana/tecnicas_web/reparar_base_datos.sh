#!/bin/bash
echo "🔧 REPARANDO BASE DE DATOS"
echo "=========================="

cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas_web

# Activar entorno virtual
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# 1. Verificar base de datos
echo "📁 Verificando base de datos..."
if [ ! -f "tecnicas_lengua.db" ]; then
    echo "⚠️ Base de datos no encontrada. Creando nueva..."
    python manage.py makemigrations
    python manage.py migrate
fi

# 2. Hacer backup
echo "💾 Haciendo backup..."
cp tecnicas_lengua.db tecnicas_lengua_backup_$(date +%Y%m%d_%H%M%S).db 2>/dev/null

# 3. Aplicar migraciones
echo "🔄 Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# 4. Importar datos
echo "📥 Importando datos..."
if python importar_datos.py; then
    echo "✅ Datos importados correctamente"
else
    echo "⚠️ Error importando datos. Intentando método alternativo..."
    python regenerar_db_completo.py
fi

# 5. Verificar
echo "🔍 Verificando..."
python manage.py shell -c "from core.models import Tecnica; print(f'Técnicas: {Tecnica.objects.count()}')"

echo ""
echo "✅ Reparación completada"
echo "🚀 Inicia el servidor: python manage.py runserver 0.0.0.0:8000"
