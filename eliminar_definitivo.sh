#!/bin/bash
echo "🔧 ELIMINANDO ARCHIVO GRANDE DEFINITIVAMENTE"

# Ir al directorio raíz
cd /workspaces/cuadernos_redaccion_lengua_castellana

# Hacer backup del .git
echo "📁 Haciendo backup de .git..."
mv .git .git_backup_$(date +%Y%m%d_%H%M%S)

# Inicializar nuevo repositorio
echo "🔄 Inicializando nuevo repositorio..."
git init

# Agregar todos los archivos excepto el grande
echo "📦 Agregando archivos..."
git add .
git rm --cached ejercicios_completos-lengua-castellana/14_miscelaneos/tails-amd64-7.8.1.img 2>/dev/null

# Eliminar físicamente el archivo
echo "🗑️ Eliminando archivo físico..."
rm -f ejercicios_completos-lengua-castellana/14_miscelaneos/tails-amd64-7.8.1.img

# Actualizar .gitignore
echo "*.img" >> .gitignore
echo "*.iso" >> .gitignore
git add .gitignore

# Hacer commit
echo "📝 Haciendo commit..."
git commit -m "Repositorio limpio - sin archivos grandes"

# Agregar remoto
echo "🌐 Configurando remoto..."
git remote add origin https://github.com/Hernank10/cuadernos_redaccion_lengua_castellana.git

# Forzar push
echo "⬆️ Subiendo a GitHub..."
git push -f origin main

echo "✅ ¡Completado!"
echo "📊 Tamaño del repositorio:"
du -sh .git
