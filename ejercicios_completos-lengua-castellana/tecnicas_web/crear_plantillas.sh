#!/bin/bash

mkdir -p core/templates/core

# Base
cat > core/templates/core/base.html << 'HTML'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo|default:"Técnicas de Lengua Castellana" }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <style>
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: all 0.3s; }
        .contenido-preview { max-height: 150px; overflow: hidden; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'core:index' %}">
                <i class="bi bi-book"></i> Técnicas Lengua Castellana
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:tecnicas_list' %}">
                            <i class="bi bi-list-ul"></i> Técnicas
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:categorias' %}">
                            <i class="bi bi-tags"></i> Categorías
                        </a>
                    </li>
                </ul>
                <form class="d-flex" action="{% url 'core:buscar' %}" method="get">
                    <input class="form-control me-2" type="search" name="q" placeholder="Buscar técnicas..." aria-label="Buscar">
                    <button class="btn btn-light" type="submit">
                        <i class="bi bi-search"></i>
                    </button>
                </form>
            </div>
        </div>
    </nav>

    <main class="py-4">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="bg-light py-3 mt-5">
        <div class="container text-center">
            <p class="text-muted mb-0">
                <i class="bi bi-database"></i> Base de datos con técnicas de lengua castellana
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
HTML

# Index
cat > core/templates/core/index.html << 'HTML'
{% extends 'core/base.html' %}
{% block content %}
<div class="row">
    <div class="col-12 text-center mb-4">
        <h1 class="display-4">📚 Técnicas de Lengua Castellana</h1>
        <p class="lead">Explora {{ total_tecnicas }} técnicas organizadas en {{ total_categorias }} categorías</p>
    </div>
</div>

<div class="row mb-4">
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-file-text"></i> Total Técnicas</h5>
                <p class="display-4">{{ total_tecnicas }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-tags"></i> Categorías</h5>
                <p class="display-4">{{ total_categorias }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-clock-history"></i> Últimas</h5>
                <p class="display-4">{{ ultimas|length }}</p>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-8">
        <h3><i class="bi bi-clock-history"></i> Últimas técnicas</h3>
        <div class="list-group">
            {% for tecnica in ultimas %}
            <a href="{% url 'core:tecnica_detail' tecnica.id %}" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ tecnica.titulo|truncatechars:80 }}</h5>
                    <span class="badge bg-primary">{{ tecnica.categoria }}</span>
                </div>
            </a>
            {% empty %}
            <p class="text-muted">No hay técnicas aún</p>
            {% endfor %}
        </div>
    </div>
    <div class="col-md-4">
        <h3><i class="bi bi-tags"></i> Categorías</h3>
        <div class="list-group">
            {% for cat in categorias|slice:":10" %}
            <a href="{% url 'core:tecnicas_list' %}?categoria={{ cat.categoria }}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                {{ cat.categoria }}
                <span class="badge bg-primary rounded-pill">{{ cat.total }}</span>
            </a>
            {% endfor %}
        </div>
        <div class="mt-3">
            <a href="{% url 'core:categorias' %}" class="btn btn-outline-primary w-100">Ver todas</a>
        </div>
    </div>
</div>
{% endblock %}
HTML

# Técnicas list
cat > core/templates/core/tecnicas_list.html << 'HTML'
{% extends 'core/base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-3">
        <h5><i class="bi bi-funnel"></i> Filtros</h5>
        <div class="list-group mb-3">
            <a href="{% url 'core:tecnicas_list' %}" class="list-group-item list-group-item-action {% if not categoria_actual %}active{% endif %}">
                Todas
            </a>
            {% for cat in categorias %}
            <a href="{% url 'core:tecnicas_list' %}?categoria={{ cat }}" class="list-group-item list-group-item-action {% if categoria_actual == cat %}active{% endif %}">
                {{ cat }}
            </a>
            {% endfor %}
        </div>
    </div>
    <div class="col-md-9">
        <h3><i class="bi bi-list-ul"></i> Técnicas</h3>
        <p class="text-muted">{{ tecnicas.paginator.count }} técnicas encontradas</p>
        
        {% for tecnica in tecnicas %}
        <div class="card card-hover mb-3">
            <div class="card-body">
                <h5 class="card-title">
                    <a href="{% url 'core:tecnica_detail' tecnica.id %}" class="text-decoration-none">
                        {{ tecnica.titulo|truncatechars:100 }}
                    </a>
                </h5>
                <span class="badge bg-primary">{{ tecnica.categoria }}</span>
                <p class="card-text mt-2 contenido-preview">
                    {{ tecnica.contenido|truncatewords:30|default:"Sin contenido" }}
                </p>
                <small class="text-muted">
                    <i class="bi bi-file-earmark"></i> {{ tecnica.tipo|default:"N/A" }}
                </small>
            </div>
        </div>
        {% empty %}
        <div class="alert alert-info">No se encontraron técnicas</div>
        {% endfor %}
        
        {% if tecnicas.has_other_pages %}
        <nav>
            <ul class="pagination">
                {% if tecnicas.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1{% if categoria_actual %}&categoria={{ categoria_actual }}{% endif %}">Primera</a>
                </li>
                {% endif %}
                <li class="page-item active">
                    <span class="page-link">{{ tecnicas.number }} de {{ tecnicas.paginator.num_pages }}</span>
                </li>
                {% if tecnicas.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ tecnicas.next_page_number }}{% if categoria_actual %}&categoria={{ categoria_actual }}{% endif %}">Siguiente</a>
                </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
    </div>
</div>
{% endblock %}
HTML

# Detalle
cat > core/templates/core/tecnica_detail.html << 'HTML'
{% extends 'core/base.html' %}
{% block content %}
<div class="row">
    <div class="col-md-12">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{% url 'core:index' %}">Inicio</a></li>
                <li class="breadcrumb-item"><a href="{% url 'core:tecnicas_list' %}">Técnicas</a></li>
                <li class="breadcrumb-item active">{{ tecnica.titulo|truncatechars:50 }}</li>
            </ol>
        </nav>
        
        <div class="card">
            <div class="card-header">
                <h3>{{ tecnica.titulo }}</h3>
                <span class="badge bg-primary">{{ tecnica.categoria }}</span>
                {% if tecnica.grado and tecnica.grado != 'General' %}
                <span class="badge bg-secondary">{{ tecnica.grado }}</span>
                {% endif %}
            </div>
            <div class="card-body">
                <pre style="white-space: pre-wrap; word-wrap: break-word; font-family: inherit;">{{ tecnica.contenido }}</pre>
                
                {% if tecnicas_json %}
                <hr>
                <h4><i class="bi bi-diagram-3"></i> Técnicas JSON</h4>
                {% for tj in tecnicas_json %}
                <div class="card mb-2">
                    <div class="card-body">
                        <h5>Técnica {{ tj.tecnica_numero }}: {{ tj.titulo_tecnica }}</h5>
                        {% if tj.teoria %}<p><strong>Teoría:</strong> {{ tj.teoria }}</p>{% endif %}
                        {% if tj.ejemplo %}<p><strong>Ejemplo:</strong> {{ tj.ejemplo }}</p>{% endif %}
                    </div>
                </div>
                {% endfor %}
                {% endif %}
            </div>
            <div class="card-footer text-muted">
                ID: {{ tecnica.id }} | {{ tecnica.fecha_creacion|date:"d/m/Y H:i" }}
            </div>
        </div>
        
        <div class="mt-3">
            <a href="{% url 'core:tecnicas_list' %}" class="btn btn-secondary">
                <i class="bi bi-arrow-left"></i> Volver
            </a>
        </div>
    </div>
</div>
{% endblock %}
HTML

# Categorías
cat > core/templates/core/categorias.html << 'HTML'
{% extends 'core/base.html' %}
{% block content %}
<h3><i class="bi bi-tags"></i> Categorías</h3>
<p class="text-muted">Explora las técnicas organizadas por categoría</p>

<div class="row">
    {% for cat in categorias %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card card-hover h-100">
            <div class="card-body">
                <h5 class="card-title">{{ cat.nombre }}</h5>
                <p><span class="badge bg-primary">{{ cat.total }} técnicas</span></p>
                <ul class="list-unstyled">
                    {% for muestra in cat.muestras %}
                    <li>
                        <a href="{% url 'core:tecnica_detail' muestra.id %}" class="text-decoration-none">
                            {{ muestra.titulo|truncatechars:60 }}
                        </a>
                    </li>
                    {% endfor %}
                </ul>
                <a href="{% url 'core:tecnicas_list' %}?categoria={{ cat.nombre }}" class="btn btn-primary btn-sm w-100">
                    Ver todas <i class="bi bi-arrow-right"></i>
                </a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
HTML

# Buscar
cat > core/templates/core/buscar.html << 'HTML'
{% extends 'core/base.html' %}
{% block content %}
<h3><i class="bi bi-search"></i> Resultados de búsqueda</h3>
<p class="text-muted">Buscando: "{{ q }}" - {{ resultados.count }} resultados</p>

{% if resultados %}
<div class="row">
    <div class="col-md-12">
        {% for tecnica in resultados %}
        <div class="card card-hover mb-3">
            <div class="card-body">
                <h5 class="card-title">
                    <a href="{% url 'core:tecnica_detail' tecnica.id %}" class="text-decoration-none">
                        {{ tecnica.titulo }}
                    </a>
                </h5>
                <span class="badge bg-primary">{{ tecnica.categoria }}</span>
                <p class="card-text mt-2">{{ tecnica.contenido|truncatewords:20|default:"Sin contenido" }}</p>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% else %}
<div class="alert alert-info">
    <i class="bi bi-info-circle"></i> No se encontraron resultados para "{{ q }}"
</div>
{% endif %}

<div class="mt-3">
    <a href="{% url 'core:index' %}" class="btn btn-secondary">
        <i class="bi bi-house"></i> Volver al inicio
    </a>
</div>
{% endblock %}
HTML

echo "✅ Plantillas creadas exitosamente"
