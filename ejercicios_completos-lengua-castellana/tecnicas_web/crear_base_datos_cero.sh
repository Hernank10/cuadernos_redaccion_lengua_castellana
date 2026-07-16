#!/bin/bash
echo "🔄 CREANDO BASE DE DATOS DESDE CERO"
echo "==================================="

cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas_web

# Activar entorno virtual
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# 1. Eliminar base de datos actual
echo "🗑️ Eliminando base de datos actual..."
rm -f tecnicas_lengua.db
rm -f db.sqlite3

# 2. Eliminar migraciones
echo "🗑️ Eliminando migraciones..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 3. Crear migraciones
echo "📝 Creando migraciones..."
python manage.py makemigrations core
python manage.py makemigrations usuarios
python manage.py makemigrations cursos
python manage.py makemigrations evaluaciones
python manage.py makemigrations progreso

# 4. Aplicar migraciones
echo "🔄 Aplicando migraciones..."
python manage.py migrate

# 5. Importar datos
echo "📥 Importando datos..."
python regenerar_db_completo.py

# 6. Verificar
echo "🔍 Verificando..."
python manage.py shell -c "from core.models import Tecnica; print(f'Técnicas: {Tecnica.objects.count()}')"

echo ""
echo "✅ Base de datos creada correctamente"
