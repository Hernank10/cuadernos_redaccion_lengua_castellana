#!/bin/bash
echo "🔄 RESETEANDO LMS - VERSIÓN FINAL"

cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas_web

# Backup
if [ -f tecnicas_lengua.db ]; then
    cp tecnicas_lengua.db tecnicas_lengua_backup_$(date +%Y%m%d_%H%M%S).db
fi

# Eliminar todo
echo "🗑️ Eliminando base de datos y migraciones..."
rm -f tecnicas_lengua.db
rm -rf core/migrations/
rm -rf usuarios/migrations/
rm -rf cursos/migrations/
rm -rf progreso/migrations/

# Crear migraciones en orden
echo "📝 Creando migraciones en orden..."
python3 manage.py makemigrations core
python3 manage.py makemigrations usuarios
python3 manage.py makemigrations cursos
python3 manage.py makemigrations progreso

# Aplicar migraciones
echo "🔄 Aplicando migraciones..."
python3 manage.py migrate

# Importar datos
echo "📥 Importando técnicas..."
python3 importar_datos.py

# Crear superusuario
echo "👤 Creando superusuario..."
python3 manage.py createsuperuser

echo "✅ ¡Reset completado!"
echo "🚀 Iniciando servidor..."
python3 manage.py runserver 0.0.0.0:8000
