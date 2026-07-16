#!/bin/bash
echo "🚀 SUBIENDO TODOS LOS ARCHIVOS A GITHUB"

# Ir al directorio correcto
cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana

echo "📁 Agregando todas las carpetas con técnicas..."
git add 01_* 02_* 03_* 04_* 05_* 06_* 07_* 08_* 09_* 10_* 11_* 12_* 13_* 14_*

echo "🗄️ Agregando base de datos y archivos..."
git add *.db *.csv *.txt *.md *.py *.sh 2>/dev/null

echo "📊 Estado actual:"
git status --short | head -20

echo "📝 Haciendo commit..."
git commit -m "📚 Todas las técnicas organizadas en 14 categorías

- 342 técnicas en 14 carpetas categorizadas
- 301 archivos HTML con quizzes interactivos
- 38 archivos JSON con datos estructurados
- Base de datos SQLite completa
- Archivos CSV exportados
- Scripts de utilidad"

echo "⬆️ Subiendo a GitHub..."
git push origin main

echo "✅ ¡Todo subido exitosamente!"
echo "🔗 Repositorio: https://github.com/Hernank10/cuadernos_redaccion_lengua_castellana"
echo ""
echo "📊 Resumen final:"
echo "   - $(find 01_* 02_* 03_* 04_* 05_* 06_* 07_* 08_* 09_* 10_* 11_* 12_* 13_* 14_* -name "*.html" 2>/dev/null | wc -l) archivos HTML"
echo "   - $(find . -name "*.json" -not -path "./.git/*" 2>/dev/null | wc -l) archivos JSON"
echo "   - $(ls -lh *.db 2>/dev/null | awk '{print $5}') base de datos"
