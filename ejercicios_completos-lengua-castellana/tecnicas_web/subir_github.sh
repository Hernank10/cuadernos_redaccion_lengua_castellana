#!/bin/bash
echo "🚀 SUBIENDO A GITHUB"

# Verificar si git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git no está instalado"
    exit 1
fi

# Verificar si hay repositorio
if [ ! -d .git ]; then
    echo "📁 Inicializando repositorio..."
    git init
fi

# Verificar si hay archivos para commit
if [ -z "$(git status --porcelain)" ]; then
    echo "⚠️ No hay cambios para commitear"
else
    echo "📦 Agregando archivos..."
    git add .
    
    echo "📝 Haciendo commit..."
    git commit -m "📚 Biblioteca de Técnicas de Lengua Castellana

- 342 técnicas organizadas en 12 categorías
- Quizzes interactivos HTML autónomos
- Catálogo con búsqueda y filtros
- Base de datos SQLite
- Diseño responsive con Bootstrap"
fi

# Verificar si existe el remoto
if ! git remote get-url origin &> /dev/null; then
    echo "🌐 Configurando remoto..."
    echo "Ingresa tu usuario de GitHub:"
    read usuario
    git remote add origin https://github.com/$usuario/tecnicas-lengua-castellana.git
fi

echo "⬆️ Subiendo a GitHub..."
git branch -M main
git push -u origin main

echo "✅ ¡Subido exitosamente!"
echo "🔗 Visita: https://github.com/$(git remote get-url origin | sed 's/.*github.com.//;s/.git//')"
