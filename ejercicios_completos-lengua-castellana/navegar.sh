#!/bin/bash
# Script para navegar rápidamente en el proyecto

function ir_tecnicas() {
    cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas
}

function ir_web() {
    cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas_web
}

function ir_scripts() {
    cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/utilidades
}

function ir_docs() {
    cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/documentacion
}

function ir_backups() {
    cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/backups
}

function iniciar_servidor() {
    cd /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana/tecnicas_web
    python manage.py runserver 0.0.0.0:8000
}

function ver_estructura() {
    tree -L 2 /workspaces/cuadernos_redaccion_lengua_castellana/ejercicios_completos-lengua-castellana
}

echo "📌 Comandos disponibles:"
echo "  ir_tecnicas    - Ir a la carpeta de técnicas"
echo "  ir_web         - Ir al proyecto Django"
echo "  ir_scripts     - Ir a la carpeta de scripts"
echo "  ir_docs        - Ir a la carpeta de documentación"
echo "  ir_backups     - Ir a la carpeta de backups"
echo "  iniciar_servidor - Iniciar el servidor Django"
echo "  ver_estructura - Ver la estructura del proyecto"
