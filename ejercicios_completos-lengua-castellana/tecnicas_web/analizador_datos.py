#!/usr/bin/env python3
"""
ANALIZADOR DE DATOS PARA LMS - Técnicas de Lengua Castellana
Genera reportes, gráficos y análisis de rendimiento
"""

import os
import sys
import django
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Sum, Q
from collections import defaultdict
import json
import plotly.express as px
import plotly.graph_objects as go

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

from core.models import Tecnica
from usuarios.models import Usuario
from cursos.models import Curso, Inscripcion, ProgresoLeccion, Certificado
from evaluaciones.models import Evaluacion, Pregunta, ResultadoEvaluacion, RespuestaUsuario

class AnalizadorDatos:
    """Analizador de datos para el LMS"""
    
    def __init__(self):
        self.df_usuarios = None
        self.df_cursos = None
        self.df_inscripciones = None
        self.df_progreso = None
        self.df_evaluaciones = None
        self.df_certificados = None
        self.df_preguntas = None
        
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga todos los datos en DataFrames"""
        print("📊 Cargando datos...")
        
        # Usuarios
        usuarios = Usuario.objects.all().values(
            'id', 'username', 'email', 'rol', 'first_name', 'last_name',
            'fecha_registro', 'puntos', 'nivel'
        )
        self.df_usuarios = pd.DataFrame(list(usuarios))
        
        # Cursos
        cursos = Curso.objects.all().values(
            'id', 'titulo', 'descripcion', 'nivel', 'duracion_horas',
            'fecha_creacion', 'publicado', 'creador_id'
        )
        self.df_cursos = pd.DataFrame(list(cursos))
        
        # Inscripciones
        inscripciones = Inscripcion.objects.all().values(
            'id', 'estudiante_id', 'curso_id', 'estado', 'progreso',
            'fecha_inscripcion', 'fecha_completado', 'calificacion'
        )
        self.df_inscripciones = pd.DataFrame(list(inscripciones))
        
        # Progreso de lecciones
        progreso = ProgresoLeccion.objects.all().values(
            'id', 'estudiante_id', 'leccion_id', 'completado',
            'fecha_completado', 'tiempo_estudio', 'intentos'
        )
        self.df_progreso = pd.DataFrame(list(progreso))
        
        # Evaluaciones
        evaluaciones = Evaluacion.objects.all().values(
            'id', 'curso_id', 'titulo', 'tipo', 'duracion_minutos',
            'fecha_creacion', 'publicado', 'puntaje_maximo'
        )
        self.df_evaluaciones = pd.DataFrame(list(evaluaciones))
        
        # Certificados
        certificados = Certificado.objects.all().values(
            'id', 'usuario_id', 'curso_id', 'codigo', 'fecha_emision',
            'fecha_completado', 'puntuacion', 'horas'
        )
        self.df_certificados = pd.DataFrame(list(certificados))
        
        # Resultados de evaluaciones
        resultados = ResultadoEvaluacion.objects.all().values(
            'id', 'usuario_id', 'evaluacion_id', 'puntaje_obtenido',
            'aprobado', 'fecha_inicio', 'fecha_completado'
        )
        self.df_resultados = pd.DataFrame(list(resultados))
        
        print(f"✅ Datos cargados:")
        print(f"   👤 Usuarios: {len(self.df_usuarios)}")
        print(f"   📚 Cursos: {len(self.df_cursos)}")
        print(f"   📝 Inscripciones: {len(self.df_inscripciones)}")
        print(f"   📖 Progreso: {len(self.df_progreso)}")
        print(f"   📋 Evaluaciones: {len(self.df_evaluaciones)}")
        print(f"   🎓 Certificados: {len(self.df_certificados)}")
    
    # ========================================
    # ANÁLISIS DE USUARIOS
    # ========================================
    
    def analizar_usuarios(self):
        """Análisis de usuarios del sistema"""
        print("\n" + "="*60)
        print("👤 ANÁLISIS DE USUARIOS")
        print("="*60)
        
        # Estadísticas generales
        total_usuarios = len(self.df_usuarios)
        estudiantes = len(self.df_usuarios[self.df_usuarios['rol'] == 'estudiante'])
        profesores = len(self.df_usuarios[self.df_usuarios['rol'] == 'profesor'])
        
        print(f"📊 Estadísticas de usuarios:")
        print(f"   Total: {total_usuarios}")
        print(f"   Estudiantes: {estudiantes}")
        print(f"   Profesores: {profesores}")
        print(f"   Admins: {total_usuarios - estudiantes - profesores}")
        
        # Usuarios por fecha de registro
        if not self.df_usuarios.empty and 'fecha_registro' in self.df_usuarios.columns:
            self.df_usuarios['fecha_registro'] = pd.to_datetime(self.df_usuarios['fecha_registro'])
            usuarios_por_dia = self.df_usuarios.groupby(
                self.df_usuarios['fecha_registro'].dt.date
            ).size()
            
            print(f"\n📈 Registros de usuarios:")
            print(f"   Promedio diario: {usuarios_por_dia.mean():.1f}")
            print(f"   Máximo en un día: {usuarios_por_dia.max()}")
        
        # Top 10 usuarios con más puntos
        if 'puntos' in self.df_usuarios.columns:
            top_puntos = self.df_usuarios.nlargest(10, 'puntos')[['username', 'puntos', 'nivel']]
            print(f"\n🏆 Top 10 usuarios por puntos:")
            for idx, row in top_puntos.iterrows():
                print(f"   {row['username']}: {row['puntos']} pts (Nivel {row['nivel']})")
        
        # Distribución de roles
        print(f"\n📊 Distribución de roles:")
        roles = self.df_usuarios['rol'].value_counts()
        for rol, count in roles.items():
            print(f"   {rol}: {count} ({count/total_usuarios*100:.1f}%)")
        
        return {
            'total_usuarios': total_usuarios,
            'estudiantes': estudiantes,
            'profesores': profesores,
            'roles': roles.to_dict()
        }
    
    # ========================================
    # ANÁLISIS DE CURSOS Y PROGRESO
    # ========================================
    
    def analizar_cursos(self):
        """Análisis de cursos y progreso"""
        print("\n" + "="*60)
        print("📚 ANÁLISIS DE CURSOS")
        print("="*60)
        
        total_cursos = len(self.df_cursos)
        publicados = len(self.df_cursos[self.df_cursos['publicado'] == True])
        
        print(f"📊 Estadísticas de cursos:")
        print(f"   Total: {total_cursos}")
        print(f"   Publicados: {publicados}")
        print(f"   No publicados: {total_cursos - publicados}")
        
        # Cursos por nivel
        if 'nivel' in self.df_cursos.columns:
            niveles = self.df_cursos['nivel'].value_counts()
            print(f"\n📊 Cursos por nivel:")
            for nivel, count in niveles.items():
                print(f"   {nivel}: {count}")
        
        # Inscripciones por curso
        if not self.df_inscripciones.empty:
            inscripciones_por_curso = self.df_inscripciones.groupby('curso_id').size()
            curso_popular = self.df_inscripciones['curso_id'].value_counts().index[0]
            curso_popular_nombre = self.df_cursos[self.df_cursos['id'] == curso_popular]['titulo'].values[0] if not self.df_cursos.empty else "Desconocido"
            
            print(f"\n📈 Inscripciones:")
            print(f"   Total: {len(self.df_inscripciones)}")
            print(f"   Promedio por curso: {inscripciones_por_curso.mean():.1f}")
            print(f"   Curso más popular: {curso_popular_nombre}")
        
        # Progreso promedio
        if not self.df_inscripciones.empty and 'progreso' in self.df_inscripciones.columns:
            progreso_promedio = self.df_inscripciones['progreso'].mean()
            completados = len(self.df_inscripciones[self.df_inscripciones['estado'] == 'completado'])
            
            print(f"\n📊 Progreso de estudiantes:")
            print(f"   Progreso promedio: {progreso_promedio:.1f}%")
            print(f"   Cursos completados: {completados}")
            print(f"   Tasa de completitud: {completados/len(self.df_inscripciones)*100:.1f}%")
        
        return {
            'total_cursos': total_cursos,
            'publicados': publicados,
            'inscripciones': len(self.df_inscripciones),
            'progreso_promedio': progreso_promedio if not self.df_inscripciones.empty else 0
        }
    
    # ========================================
    # ANÁLISIS DE EVALUACIONES
    # ========================================
    
    def analizar_evaluaciones(self):
        """Análisis de evaluaciones y rendimiento"""
        print("\n" + "="*60)
        print("📝 ANÁLISIS DE EVALUACIONES")
        print("="*60)
        
        total_evaluaciones = len(self.df_evaluaciones)
        publicadas = len(self.df_evaluaciones[self.df_evaluaciones['publicado'] == True])
        
        print(f"📊 Estadísticas de evaluaciones:")
        print(f"   Total: {total_evaluaciones}")
        print(f"   Publicadas: {publicadas}")
        
        # Evaluaciones por tipo
        if 'tipo' in self.df_evaluaciones.columns:
            tipos = self.df_evaluaciones['tipo'].value_counts()
            print(f"\n📊 Evaluaciones por tipo:")
            for tipo, count in tipos.items():
                print(f"   {tipo}: {count}")
        
        # Resultados
        if not self.df_resultados.empty:
            promedio = self.df_resultados['puntaje_obtenido'].mean()
            aprobados = len(self.df_resultados[self.df_resultados['aprobado'] == True])
            
            print(f"\n📊 Resultados de evaluaciones:")
            print(f"   Total resultados: {len(self.df_resultados)}")
            print(f"   Puntaje promedio: {promedio:.1f}%")
            print(f"   Aprobados: {aprobados}")
            print(f"   Tasa de aprobación: {aprobados/len(self.df_resultados)*100:.1f}%")
        
        return {
            'total_evaluaciones': total_evaluaciones,
            'publicadas': publicadas,
            'promedio_puntaje': promedio if not self.df_resultados.empty else 0,
            'tasa_aprobacion': aprobados/len(self.df_resultados)*100 if not self.df_resultados.empty else 0
        }
    
    # ========================================
    # ANÁLISIS DE CERTIFICADOS
    # ========================================
    
    def analizar_certificados(self):
        """Análisis de certificados"""
        print("\n" + "="*60)
        print("🎓 ANÁLISIS DE CERTIFICADOS")
        print("="*60)
        
        total_certificados = len(self.df_certificados)
        
        print(f"📊 Estadísticas de certificados:")
        print(f"   Total: {total_certificados}")
        
        if not self.df_certificados.empty:
            # Certificados por mes
            self.df_certificados['fecha_emision'] = pd.to_datetime(self.df_certificados['fecha_emision'])
            certificados_por_mes = self.df_certificados.groupby(
                self.df_certificados['fecha_emision'].dt.to_period('M')
            ).size()
            
            print(f"\n📈 Certificados emitidos por mes:")
            for mes, count in certificados_por_mes.items():
                print(f"   {mes}: {count}")
            
            # Puntuación promedio
            puntuacion_promedio = self.df_certificados['puntuacion'].mean()
            print(f"\n📊 Puntuación promedio: {puntuacion_promedio:.1f}%")
        
        return {
            'total_certificados': total_certificados
        }
    
    # ========================================
    # GENERACIÓN DE GRÁFICOS
    # ========================================
    
    def generar_graficos(self, output_dir="static/img/analisis"):
        """Genera gráficos de análisis"""
        print("\n" + "="*60)
        print("📊 GENERANDO GRÁFICOS")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Distribución de usuarios por rol
        if not self.df_usuarios.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            roles = self.df_usuarios['rol'].value_counts()
            ax.pie(roles.values, labels=roles.index, autopct='%1.1f%%', startangle=90)
            ax.set_title('Distribución de Usuarios por Rol')
            plt.savefig(f"{output_dir}/distribucion_roles.png")
            print("✅ Gráfico 1: Distribución de roles")
        
        # 2. Cursos por nivel
        if not self.df_cursos.empty and 'nivel' in self.df_cursos.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            niveles = self.df_cursos['nivel'].value_counts()
            ax.bar(niveles.index, niveles.values)
            ax.set_title('Cursos por Nivel')
            ax.set_xlabel('Nivel')
            ax.set_ylabel('Número de Cursos')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/cursos_por_nivel.png")
            print("✅ Gráfico 2: Cursos por nivel")
        
        # 3. Progreso de estudiantes
        if not self.df_inscripciones.empty and 'progreso' in self.df_inscripciones.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(self.df_inscripciones['progreso'], bins=20, edgecolor='black')
            ax.set_title('Distribución de Progreso de Estudiantes')
            ax.set_xlabel('Progreso (%)')
            ax.set_ylabel('Número de Inscripciones')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/progreso_estudiantes.png")
            print("✅ Gráfico 3: Progreso de estudiantes")
        
        # 4. Resultados de evaluaciones
        if not self.df_resultados.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(self.df_resultados['puntaje_obtenido'], bins=20, edgecolor='black')
            ax.set_title('Distribución de Puntajes en Evaluaciones')
            ax.set_xlabel('Puntaje (%)')
            ax.set_ylabel('Número de Resultados')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/puntajes_evaluaciones.png")
            print("✅ Gráfico 4: Puntajes de evaluaciones")
        
        print(f"✅ Gráficos guardados en: {output_dir}")
    
    # ========================================
    # GENERACIÓN DE REPORTES
    # ========================================
    
    def generar_reporte_completo(self):
        """Genera un reporte completo en formato JSON"""
        print("\n" + "="*60)
        print("📋 GENERANDO REPORTE COMPLETO")
        print("="*60)
        
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'estadisticas': {
                'usuarios': self.analizar_usuarios(),
                'cursos': self.analizar_cursos(),
                'evaluaciones': self.analizar_evaluaciones(),
                'certificados': self.analizar_certificados()
            },
            'datos_graficos': {}
        }
        
        # Guardar reporte
        with open('reporte_lms.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False, default=str)
        
        print("✅ Reporte guardado en: reporte_lms.json")
        
        return reporte
    
    # ========================================
    # DASHBOARD INTERACTIVO
    # ========================================
    
    def crear_dashboard(self):
        """Crea un dashboard interactivo con Plotly"""
        print("\n" + "="*60)
        print("📊 CREANDO DASHBOARD INTERACTIVO")
        print("="*60)
        
        # Crear figura de usuarios
        if not self.df_usuarios.empty:
            fig1 = px.pie(
                self.df_usuarios, 
                names='rol', 
                title='Distribución de Usuarios por Rol',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
        
        # Crear figura de cursos por nivel
        if not self.df_cursos.empty and 'nivel' in self.df_cursos.columns:
            niveles_df = self.df_cursos['nivel'].value_counts().reset_index()
            niveles_df.columns = ['Nivel', 'Cantidad']
            fig2 = px.bar(
                niveles_df,
                x='Nivel',
                y='Cantidad',
                title='Cursos por Nivel',
                color='Nivel',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
        
        # Crear figura de progreso
        if not self.df_inscripciones.empty and 'progreso' in self.df_inscripciones.columns:
            fig3 = px.histogram(
                self.df_inscripciones,
                x='progreso',
                title='Distribución de Progreso',
                nbins=20,
                color_discrete_sequence=['#6C63FF']
            )
        
        print("✅ Dashboard creado")
        print("📊 Para ver el dashboard, usa un visor de Jupyter Notebooks")
        print("   o guarda los gráficos como HTML")
        
        # Guardar como HTML
        if not self.df_usuarios.empty:
            fig1.write_html("dashboard_usuarios.html")
            print("📁 Dashboard de usuarios guardado: dashboard_usuarios.html")

def main():
    """Función principal"""
    print("="*60)
    print("📊 ANALIZADOR DE DATOS LMS")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60)
    
    analizador = AnalizadorDatos()
    
    # Análisis
    analizador.analizar_usuarios()
    analizador.analizar_cursos()
    analizador.analizar_evaluaciones()
    analizador.analizar_certificados()
    
    # Generar gráficos
    analizador.generar_graficos()
    
    # Generar reporte
    reporte = analizador.generar_reporte_completo()
    
    # Crear dashboard
    analizador.crear_dashboard()
    
    print("\n" + "="*60)
    print("✅ ANÁLISIS COMPLETADO")
    print("📊 Reportes disponibles:")
    print("   - reporte_lms.json (datos estructurados)")
    print("   - static/img/analisis/ (gráficos)")
    print("   - dashboard_usuarios.html (dashboard interactivo)")
    print("="*60)

if __name__ == "__main__":
    main()
