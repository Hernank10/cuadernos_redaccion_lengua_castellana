#!/bin/bash
echo "🗂️ ORGANIZANDO PROYECTO"

cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana

# 1. Mover carpetas de técnicas a una carpeta principal
mkdir -p tecnicas
mv 01_tecnicas_generales tecnicas/
mv 02_gramatica_morfosintaxis tecnicas/
mv 03_ortografia tecnicas/
mv 04_redaccion_cientifica tecnicas/
mv 05_redaccion_por_grados tecnicas/
mv 06_literatura_narrativa tecnicas/
mv 07_retorica_figuras tecnicas/
mv 08_comprension_lectora tecnicas/
mv 09_ingles_bilingue tecnicas/
mv 10_ciencia_ficcion tecnicas/
mv 11_educacion_colombia tecnicas/
mv 12_json_datos tecnicas/
mv 13_cuadernos_html tecnicas/
mv 14_miscelaneos tecnicas/

# 2. Mover scripts y utilidades
mkdir -p utilidades
mv *.sh utilidades/ 2>/dev/null
mv *.py utilidades/ 2>/dev/null
mv *.jar utilidades/ 2>/dev/null

# 3. Mover documentación
mkdir -p documentacion
mv *.md documentacion/ 2>/dev/null
mv *.txt documentacion/ 2>/dev/null
mv *.csv documentacion/ 2>/dev/null

# 4. Mover backups
mkdir -p backups
mv *.db backups/ 2>/dev/null
mv *.bak backups/ 2>/dev/null

# 5. Limpiar archivos temporales
rm -f *.tmp *.log *.cache 2>/dev/null

echo "✅ Proyecto organizado"
echo ""
echo "📁 Estructura final:"
ls -la
