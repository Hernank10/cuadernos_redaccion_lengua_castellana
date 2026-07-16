"""
Generador de Certificados PDF
"""

import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from django.conf import settings

class GeneradorCertificado:
    """Generador de certificados PDF"""
    
    def __init__(self, certificado):
        self.certificado = certificado
        self.usuario = certificado.usuario
        self.curso = certificado.curso
        self.buffer = BytesIO()
        
    def generar(self):
        """Genera el PDF del certificado"""
        # Crear documento en formato apaisado
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=landscape(A4),
            leftMargin=1*cm,
            rightMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm,
        )
        
        # Elementos del documento
        elementos = []
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo para título principal
        titulo_style = ParagraphStyle(
            'TituloStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=36,
            textColor=colors.HexColor('#6C63FF'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Estilo para subtítulo
        subtitulo_style = ParagraphStyle(
            'SubtituloStyle',
            parent=styles['Heading2'],
            fontName='Helvetica',
            fontSize=18,
            textColor=colors.HexColor('#2D3436'),
            alignment=TA_CENTER,
            spaceAfter=10
        )
        
        # Estilo para nombre del estudiante
        nombre_style = ParagraphStyle(
            'NombreStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=48,
            textColor=colors.HexColor('#FF6584'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Estilo para texto normal
        texto_style = ParagraphStyle(
            'TextoStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=14,
            textColor=colors.HexColor('#2D3436'),
            alignment=TA_CENTER,
            spaceAfter=10
        )
        
        # Estilo para código
        codigo_style = ParagraphStyle(
            'CodigoStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#6C757D'),
            alignment=TA_CENTER,
            spaceAfter=5
        )
        
        # 1. Título del certificado
        elementos.append(Paragraph("CERTIFICADO DE FINALIZACIÓN", titulo_style))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 2. Subtítulo
        elementos.append(Paragraph("El siguiente certificado se otorga a:", subtitulo_style))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 3. Nombre del estudiante
        nombre_completo = f"{self.usuario.first_name} {self.usuario.last_name}".strip()
        if not nombre_completo:
            nombre_completo = self.usuario.username
        elementos.append(Paragraph(nombre_completo, nombre_style))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 4. Texto descriptivo
        elementos.append(Paragraph(
            f"Por haber completado exitosamente el curso:",
            texto_style
        ))
        elementos.append(Spacer(1, 0.3*cm))
        
        # 5. Nombre del curso
        curso_style = ParagraphStyle(
            'CursoStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#4ECDC4'),
            alignment=TA_CENTER,
            spaceAfter=10
        )
        elementos.append(Paragraph(self.curso.titulo, curso_style))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 6. Detalles del curso
        detalles = [
            f"📅 Fecha de finalización: {self.certificado.fecha_completado.strftime('%d de %B de %Y')}",
            f"⏱️ Duración: {self.curso.duracion_horas} horas",
            f"📊 Calificación: {self.certificado.puntuacion:.1f}%",
            f"🔑 Código de verificación: {self.certificado.codigo}"
        ]
        
        for detalle in detalles:
            elementos.append(Paragraph(detalle, texto_style))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 7. Mensaje final
        elementos.append(Paragraph(
            "Este certificado acredita que el estudiante ha demostrado las competencias necesarias",
            texto_style
        ))
        elementos.append(Paragraph(
            "en las técnicas de lengua castellana cubiertas durante el curso.",
            texto_style
        ))
        elementos.append(Spacer(1, 1*cm))
        
        # 8. Línea de firma
        firma_style = ParagraphStyle(
            'FirmaStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.HexColor('#2D3436'),
            alignment=TA_CENTER,
            spaceAfter=5
        )
        
        elementos.append(Paragraph("_________________________", firma_style))
        elementos.append(Paragraph("Firma del Instructor", firma_style))
        elementos.append(Spacer(1, 0.5*cm))
        
        # 9. Logo / Marca de agua
        elementos.append(Paragraph(
            "Técnicas de Lengua Castellana - LMS",
            codigo_style
        ))
        
        # 10. Código de verificación
        elementos.append(Paragraph(
            f"Verificar en: https://github.com/Hernank10/cuadernos_redaccion_lengua_castellana",
            codigo_style
        ))
        
        # Generar PDF
        doc.build(elementos)
        
        # Guardar el PDF
        pdf_content = self.buffer.getvalue()
        self.buffer.close()
        
        # Crear archivo para guardar
        filename = f"certificado_{self.usuario.username}_{self.curso.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.certificado.pdf_file.save(filename, ContentFile(pdf_content))
        
        return self.certificado
