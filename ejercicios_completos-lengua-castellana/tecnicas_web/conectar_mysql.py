#!/usr/bin/env python3
"""
CONEXIÓN A MySQL PARA ANÁLISIS DE DATOS
"""

import os
import sys
import django
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnicas_web.settings')
django.setup()

def conectar_mysql():
    """Conecta a MySQL y exporta datos"""
    
    # Configurar conexión MySQL
    DB_NAME = 'tecnicas_lengua_lms'
    DB_USER = 'lms_user'
    DB_PASSWORD = 'Lms2024Secure!'
    DB_HOST = 'localhost'
    DB_PORT = '3306'
    
    try:
        # Crear conexión SQLAlchemy
        engine = create_engine(
            f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )
        
        print("✅ Conexión a MySQL establecida")
        
        # Exportar datos desde Django a MySQL
        from core.models import Tecnica
        from usuarios.models import Usuario
        from cursos.models import Curso, Inscripcion, ProgresoLeccion, Certificado
        from evaluaciones.models import Evaluacion, ResultadoEvaluacion
        
        # Convertir datos a DataFrames
        print("📊 Exportando datos a MySQL...")
        
        # Usuarios
        df_usuarios = pd.DataFrame(list(Usuario.objects.all().values()))
        df_usuarios.to_sql('analisis_usuarios', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Usuarios: {len(df_usuarios)} registros")
        
        # Cursos
        df_cursos = pd.DataFrame(list(Curso.objects.all().values()))
        df_cursos.to_sql('analisis_cursos', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Cursos: {len(df_cursos)} registros")
        
        # Inscripciones
        df_inscripciones = pd.DataFrame(list(Inscripcion.objects.all().values()))
        df_inscripciones.to_sql('analisis_inscripciones', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Inscripciones: {len(df_inscripciones)} registros")
        
        # Progreso
        df_progreso = pd.DataFrame(list(ProgresoLeccion.objects.all().values()))
        df_progreso.to_sql('analisis_progreso', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Progreso: {len(df_progreso)} registros")
        
        # Evaluaciones
        df_evaluaciones = pd.DataFrame(list(Evaluacion.objects.all().values()))
        df_evaluaciones.to_sql('analisis_evaluaciones', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Evaluaciones: {len(df_evaluaciones)} registros")
        
        # Resultados
        df_resultados = pd.DataFrame(list(ResultadoEvaluacion.objects.all().values()))
        df_resultados.to_sql('analisis_resultados', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Resultados: {len(df_resultados)} registros")
        
        # Certificados
        df_certificados = pd.DataFrame(list(Certificado.objects.all().values()))
        df_certificados.to_sql('analisis_certificados', con=engine, if_exists='replace', index=False)
        print(f"   ✅ Certificados: {len(df_certificados)} registros")
        
        print("\n✅ Datos exportados exitosamente a MySQL")
        print(f"📊 Tablas creadas en la base de datos: {DB_NAME}")
        
        # Consultas de ejemplo
        print("\n📋 Consultas de ejemplo:")
        with engine.connect() as conn:
            # Usuarios por rol
            result = pd.read_sql("SELECT rol, COUNT(*) as total FROM analisis_usuarios GROUP BY rol", conn)
            print("\n👤 Usuarios por rol:")
            print(result)
            
            # Cursos publicados
            result = pd.read_sql("SELECT COUNT(*) as publicados FROM analisis_cursos WHERE publicado = 1", conn)
            print(f"\n📚 Cursos publicados: {result['publicados'].iloc[0]}")
            
            # Progreso promedio
            result = pd.read_sql("SELECT AVG(progreso) as promedio FROM analisis_inscripciones", conn)
            print(f"📊 Progreso promedio: {result['promedio'].iloc[0]:.1f}%")
        
        return engine
        
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        print("\n💡 Si MySQL no está disponible, usa SQLite:")
        print("   python analizador_datos.py")
        return None

if __name__ == "__main__":
    conectar_mysql()
