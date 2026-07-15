# 📚 Cuadernos de Redacción - Lengua Castellana

[![GitHub](https://img.shields.io/badge/GitHub-Repositorio-blue?style=for-the-badge&logo=github)](https://github.com/Hernank10/cuadernos_redaccion_lengua_castellana)
[![Django](https://img.shields.io/badge/Django-6.0-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.45-blue?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)

## 📖 Descripción

**Biblioteca digital de técnicas de lengua castellana** con más de **342 recursos educativos** organizados en **14 categorías**. Cada técnica es un **quiz interactivo autónomo** diseñado para practicar y aprender.

### 🎯 Características Principales

- ✅ **342 técnicas** de lengua castellana
- ✅ **14 categorías** organizadas temáticamente
- ✅ **Quizzes interactivos** HTML autónomos
- ✅ **Proyecto Django** para navegación y búsqueda
- ✅ **Base de datos SQLite** con todas las técnicas
- ✅ **Diseño responsive** con Bootstrap

## 📂 Estructura del Proyecto

tecnicas_web/
├── core/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas
│   ├── urls.py             # URLs
│   └── templates/          # Plantillas HTML
├── tecnicas_web/           # Configuración del proyecto
├── static/                 # Archivos estáticos
├── tecnicas_lengua.db      # Base de datos SQLite
└── manage.pycuadernos_redaccion_lengua_castellana/
├── 📁 ejercicios_completos-lengua-castellana/
│ ├── 📁 01_tecnicas_generales/ # 95 técnicas generales
│ ├── 📁 02_gramatica_morfosintaxis/ # 37 técnicas de gramática
│ ├── 📁 03_ortografia/ # 30 técnicas de ortografía
│ ├── 📁 04_redaccion_cientifica/ # 10 técnicas científicas
│ ├── 📁 05_redaccion_por_grados/ # Técnicas por nivel educativo
│ ├── 📁 06_literatura_narrativa/ # 23 técnicas literarias
│ ├── 📁 07_retorica_figuras/ # 21 técnicas retóricas
│ ├── 📁 08_comprension_lectora/ # 2 técnicas de comprensión
│ ├── 📁 09_ingles_bilingue/ # 22 técnicas bilingües
│ ├── 📁 10_ciencia_ficcion/ # 35 técnicas de ciencia ficción
│ ├── 📁 11_educacion_colombia/ # 24 técnicas para Colombia
│ ├── 📁 12_json_datos/ # 23 archivos JSON
│ ├── 📁 13_cuadernos_html/ # 20 cuadernos HTML
│ ├── 📁 14_miscelaneos/ # Archivos varios
│ ├── 📁 tecnicas_web/ # Proyecto Django
│ ├── 📄 tecnicas_lengua.db # Base de datos SQLite
│ └── 📄 README.md # Esta documentación
└── 📄 .gitignore

text

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/Hernank10/cuadernos_redaccion_lengua_castellana.git
cd cuadernos_redaccion_lengua_castellana
2. Explorar las técnicas
bash
# Ver las carpetas organizadas
ls -la ejercicios_completos-lengua-castellana/01_*

# Ver técnicas de una categoría específica
ls ejercicios_completos-lengua-castellana/02_gramatica_morfosintaxis/
3. Ejecutar el sitio web Django
bash
cd ejercicios_completos-lengua-castellana/tecnicas_web

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py migrate

# Importar técnicas (si es necesario)
python manage.py importar_datos.py

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
4. Abrir en el navegador
text
http://localhost:8000
📊 Estadísticas del Proyecto
Categoría	Cantidad
Técnicas Generales	95
Gramática y Sintaxis	37
Ciencia Ficción	35
Ortografía	30
Educación Colombia	24
Literatura y Narrativa	23
JSON	23
Inglés Bilingüe	22
Retórica y Figuras	21
Cuadernos	20
Redacción Científica	10
Comprensión Lectora	2
TOTAL	342
🎯 Cómo Usar los Quizzes
Explora las técnicas desde el sitio web Django

Filtra por categoría o busca por palabra clave

Haz clic en "Ver Quiz" para abrir el interactivo

Practica con las 100 técnicas y ejercicios

Cada quiz incluye:

✅ 100 técnicas de práctica

✅ Tarjetas flashcard interactivas

✅ Ejercicios de opción múltiple

✅ Retroalimentación inmediata

✅ Diseño autónomo y responsive

🛠️ Tecnologías Utilizadas
Backend: Django 6.0

Frontend: Bootstrap 5, HTML5, CSS3, JavaScript

Base de datos: SQLite 3.45

Lenguaje: Python 3.12+

Control de versiones: Git

📦 Dependencias
txt
Django>=6.0,<7.0
beautifulsoup4>=4.12.0
mysql-connector-python>=8.0.0
🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si deseas agregar nuevas técnicas o mejorar el proyecto:

Fork el repositorio

Crea una rama (git checkout -b feature/nueva-tecnica)

Commit tus cambios (git commit -m 'Agregar nueva técnica')

Push a la rama (git push origin feature/nueva-tecnica)

Abre un Pull Request

📝 Licencia
Este proyecto es de uso educativo y libre. Puedes usarlo, modificarlo y compartirlo libremente.

👤 Autor
Hernán Acevedo Marín

GitHub: @Hernank10

🙏 Agradecimientos
A todos los que contribuyen con el aprendizaje de la lengua castellana

A la comunidad de Django y Python por su excelente trabajo

📞 Contacto
Para preguntas o sugerencias:

GitHub Issues: Crear Issue

⭐ Si este proyecto te ha sido útil, no olvides darle una estrella en GitHub!
