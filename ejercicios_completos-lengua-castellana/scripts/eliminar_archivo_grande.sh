#!/bin/bash
echo "🔧 ELIMINANDO ARCHIVO GRANDE DEL HISTORIAL"

# 1. Eliminar el archivo del área de staging
echo "📁 Eliminando archivo del área de staging..."
git rm --cached ejercicios_completos-lengua-castellana/14_miscelaneos/tails-amd64-7.8.1.img 2>/dev/null

# 2. Eliminar el archivo físico
echo "🗑️ Eliminando archivo físico..."
rm -f ejercicios_completos-lengua-castellana/14_miscelaneos/tails-amd64-7.8.1.img

# 3. Eliminar del historial
echo "📝 Eliminando del historial de Git..."
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch ejercicios_completos-lengua-castellana/14_miscelaneos/tails-amd64-7.8.1.img" \
  --prune-empty --tag-name-filter cat -- --all 2>/dev/null

# 4. Limpiar
echo "🧹 Limpiando repositorio..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Actualizar .gitignore
echo "📄 Actualizando .gitignore..."
echo "*.img" >> .gitignore
echo "*.iso" >> .gitignore
git add .gitignore
git commit -m "Ignorar archivos .img e .iso grandes"

echo "✅ Archivo grande eliminado del historial"
echo "🚀 Ahora ejecuta: git push origin main --force"
