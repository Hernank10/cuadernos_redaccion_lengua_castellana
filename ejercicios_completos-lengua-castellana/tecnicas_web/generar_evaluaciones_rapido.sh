#!/bin/bash
echo "🧠 GENERADOR AUTOMÁTICO DE EVALUACIONES"
echo "========================================"

cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas_web

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar el generador
python3 generar_evaluaciones.py

echo ""
echo "✅ Evaluaciones generadas exitosamente"
echo "🔍 Revisa en: http://localhost:8000/admin/evaluaciones/"
