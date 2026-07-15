#!/usr/bin/env python3
"""
Generador Avanzado de Evaluaciones
Con opciones de personalización y exportación
"""

import os
import sys
import json
import random
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica
from cursos.models import Curso
from evaluaciones.models import Evaluacion, Pregunta
from usuarios.models import Usuario

class GeneradorAvanzado:
    """Generador avanzado con opciones de personalización"""
    
    def __init__(self):
        self.tecnicas = Tecnica.objects.all()
        self.admin = Usuario.objects.filter(is_superuser=True).first()
        
        print("🧠 GENERADOR AVANZADO DE EVALUACIONES")
        print("="*60)
        print(f"📚 Técnicas disponibles: {self.tecnicas.count()}")
        print(f"👤 Admin: {self.admin.username if self.admin else 'No encontrado'}")
        print("="*60)
    
    def generar_por_dificultad(self, curso, nivel='intermedio', num_preguntas=10):
        """Genera evaluación con preguntas de un nivel específico"""
        # Filtrar técnicas por nivel
        if nivel == 'facil':
            tecnicas = curso.tecnicas.filter(grado__icontains='básico')[:20]
        elif nivel == 'intermedio':
            tecnicas = curso.tecnicas.filter(grado__icontains='intermedio')[:20]
        elif nivel == 'avanzado':
            tecnicas = curso.tecnicas.filter(grado__icontains='avanzado')[:20]
        else:
            tecnicas = curso.tecnicas.all()[:20]
        
        return self._crear_evaluacion(curso, tecnicas, num_preguntas, f"Evaluación {nivel.title()}")
    
    def generar_mixta(self, curso, num_preguntas=10):
        """Genera evaluación con preguntas de diferentes tipos"""
        tipos = ['multiple', 'verdadero_falso', 'completar', 'abierta']
        preguntas_por_tipo = max(1, num_preguntas // len(tipos))
        
        return self._crear_evaluacion_con_tipos(curso, tipos, preguntas_por_tipo)
    
    def _crear_evaluacion(self, curso, tecnicas, num_preguntas, titulo_sufijo):
        """Método auxiliar para crear evaluación"""
        # ... (implementación similar al generador principal)
        pass
    
    def _crear_evaluacion_con_tipos(self, curso, tipos, preguntas_por_tipo):
        """Crea evaluación con tipos específicos de preguntas"""
        # ... (implementación específica)
        pass

if __name__ == "__main__":
    generador = GeneradorAvanzado()
    print("✅ Generador avanzado listo para usar")
