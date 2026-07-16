# 📁 Estructura del Proyecto

## Organización de Archivos y Carpetas

cuadernos_redaccion_lengua_castellana/
│
├── 📁 ejercicios_completos-lengua-castellana/
│ ├── 📁 tecnicas/ # Todas las técnicas organizadas
│ │ ├── 01_tecnicas_generales/
│ │ ├── 02_gramatica_morfosintaxis/
│ │ ├── 03_ortografia/
│ │ ├── 04_redaccion_cientifica/
│ │ ├── 05_redaccion_por_grados/
│ │ ├── 06_literatura_narrativa/
│ │ ├── 07_retorica_figuras/
│ │ ├── 08_comprension_lectora/
│ │ ├── 09_ingles_bilingue/
│ │ ├── 10_ciencia_ficcion/
│ │ ├── 11_educacion_colombia/
│ │ ├── 12_json_datos/
│ │ ├── 13_cuadernos_html/
│ │ └── 14_miscelaneos/
│ │
│ ├── 📁 tecnicas_web/ # Proyecto Django
│ │ ├── core/
│ │ ├── usuarios/
│ │ ├── cursos/
│ │ ├── evaluaciones/
│ │ ├── generador/
│ │ ├── static/
│ │ ├── media/
│ │ ├── manage.py
│ │ └── requirements.txt
│ │
│ ├── 📁 utilidades/ # Scripts y herramientas
│ │ ├── *.py
│ │ ├── *.sh
│ │ └── *.jar
│ │
│ ├── 📁 documentacion/ # Documentación
│ │ ├── README.md
│ │ ├── estructura_completa.txt
│ │ └── index_tecnicas.md
│ │
│ └── 📁 backups/ # Backups de base de datos
│ ├── *.db
│ └── *.csv
│
└── 📁 scripts/ # Scripts principales
├── navegar.sh
├── organizar_proyecto.sh
└── instalar_lms.sh

## 🚀 Navegación Rápida

```bash
source navegar.sh  # Cargar funciones
ir_tecnicas        # Ir a técnicas
ir_web             # Ir a Django
ir_scripts         # Ir a scripts
ir_docs            # Ir a documentación
ir_backups         # Ir a backups
iniciar_servidor   # Iniciar servidor
ver_estructura     # Ver estructura

## 🧹 **Paso 5: Limpieza final**

```bash
# Ejecutar limpieza completa
cat > limpiar_proyecto.sh << 'EOF'
#!/bin/bash
echo "🧹 LIMPIANDO PROYECTO"

cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana

# Eliminar archivos temporales
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.tmp" -delete
find . -name "*.log" -delete
find . -name "*.cache" -delete

# Eliminar migraciones viejas
find tecnicas_web -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null

# Comprimir logs antiguos
find . -name "*.log" -exec gzip {} \; 2>/dev/null

echo "✅ Limpieza completada"
echo ""
echo "📊 Espacio liberado:"
du -sh . 2>/dev/null || echo "No se pudo calcular"
