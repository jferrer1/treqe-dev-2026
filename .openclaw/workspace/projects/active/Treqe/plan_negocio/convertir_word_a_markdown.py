#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte documento Word de Treqe a Markdown para análisis óptimo.
"""

import docx
import os
import re
from datetime import datetime

def convertir_word_a_markdown():
    """Convierte el último documento Word a Markdown."""
    input_path = "Plan_Negocio_Treqe_CON_EXPLICACIONES_EXTENDIDAS_2026.docx"
    output_path = "Treqe_Plan_Negocio_ANALISIS.md"
    
    if not os.path.exists(input_path):
        print(f"Error: Documento no encontrado: {input_path}")
        return None
    
    print(f"Convirtiendo: {input_path} -> {output_path}")
    print("="*60)
    
    # Cargar documento
    doc = docx.Document(input_path)
    
    # Preparar contenido Markdown
    markdown_lines = []
    
    # Contador de secciones
    secciones = 0
    parrafos = 0
    listas = 0
    
    # Mapeo de estilos Word → Markdown
    def estilo_a_markdown(estilo_nombre, texto):
        if not estilo_nombre:
            return texto
        
        estilo_nombre = estilo_nombre.lower()
        
        # Encabezados
        if 'heading 1' in estilo_nombre:
            return f"# {texto}"
        elif 'heading 2' in estilo_nombre:
            return f"## {texto}"
        elif 'heading 3' in estilo_nombre:
            return f"### {texto}"
        elif 'heading 4' in estilo_nombre:
            return f"#### {texto}"
        elif 'heading 5' in estilo_nombre:
            return f"##### {texto}"
        elif 'heading 6' in estilo_nombre:
            return f"###### {texto}"
        elif 'title' in estilo_nombre:
            return f"# {texto}"
        elif 'subtitle' in estilo_nombre:
            return f"## {texto}"
        else:
            return texto
    
    # Procesar cada párrafo
    for i, para in enumerate(doc.paragraphs):
        texto = para.text.strip()
        
        if not texto:  # Párrafo vacío
            markdown_lines.append("")
            continue
        
        # Determinar estilo
        estilo = para.style.name if para.style else None
        
        # Verificar si es item de lista
        es_lista = False
        if para.text.startswith('- ') or para.text.startswith('• ') or para.text.startswith('* '):
            es_lista = True
            listas += 1
        elif any(char in para.text[:10] for char in ['-', '•', '*', '✓', '→', '▶']):
            # Verificar si comienza con caracter de lista en primeros 10 caracteres
            es_lista = True
            listas += 1
        
        # Aplicar conversión
        if es_lista:
            # Mantener formato de lista
            markdown_lines.append(texto)
        elif estilo:
            # Aplicar estilo Markdown
            markdown_text = estilo_a_markdown(estilo, texto)
            markdown_lines.append(markdown_text)
            
            if 'heading' in estilo.lower() or 'title' in estilo.lower():
                secciones += 1
        else:
            # Párrafo normal
            markdown_lines.append(texto)
        
        parrafos += 1
    
    # Agregar metadatos al inicio
    metadata = [
        f"# TREQE - PLAN DE NEGOCIO (ANÁLISIS OPTIMIZADO)",
        "",
        f"**Fecha conversión:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Documento original:** {input_path}",
        f"**Total secciones:** {secciones}",
        f"**Total párrafos:** {parrafos}",
        f"**Elementos lista:** {listas}",
        "",
        "---",
        ""
    ]
    
    contenido_final = metadata + markdown_lines
    
    # Guardar como Markdown
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido_final))
    
    # Crear versión simplificada para análisis rápido
    output_simple = "Treqe_Plan_Negocio_ANALISIS_SIMPLE.md"
    
    # Extraer solo encabezados y puntos clave para vista rápida
    lineas_simplificadas = []
    for linea in contenido_final:
        # Incluir todos los encabezados
        if linea.startswith('#') or 'APÉNDICE' in linea.upper() or 'FASE' in linea.upper():
            lineas_simplificadas.append(linea)
        # Incluir puntos clave (listas que contienen palabras importantes)
        elif any(palabra in linea.lower() for palabra in ['score', 'fórmula', 'algoritmo', 'ventaja', 'ejemplo', 'nivel']):
            lineas_simplificadas.append(f"  {linea}")
    
    with open(output_simple, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_simplificadas))
    
    # Crear índice de contenido
    indice_path = "Treqe_Plan_Negocio_INDICE.md"
    
    indice = ["# ÍNDICE DEL DOCUMENTO TREQE", "", "## ESTRUCTURA PRINCIPAL", ""]
    
    # Extraer estructura jerárquica
    nivel_actual = 0
    for linea in contenido_final:
        if linea.startswith('# '):
            indice.append(f"1. **{linea[2:]}**")
            nivel_actual = 1
        elif linea.startswith('## '):
            indice.append(f"   1.{nivel_actual} {linea[3:]}")
            nivel_actual += 1
        elif linea.startswith('### '):
            indice.append(f"       - {linea[4:]}")
    
    with open(indice_path, "w", encoding="utf-8") as f:
        f.write("\n".join(indice))
    
    # Crear reporte
    reporte_path = "reporte_conversion_markdown.txt"
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write(f"REPORTE DE CONVERSIÓN A MARKDOWN\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Documento Word: {input_path}\n")
        f.write(f"Markdown completo: {output_path}\n")
        f.write(f"Markdown simplificado: {output_simple}\n")
        f.write(f"Índice: {indice_path}\n")
        f.write(f"Tamaño Word: {os.path.getsize(input_path):,} bytes\n")
        f.write(f"Tamaño Markdown: {os.path.getsize(output_path):,} bytes\n")
        f.write(f"Compresión: {os.path.getsize(output_path)/os.path.getsize(input_path)*100:.1f}%\n")
        f.write(f"Secciones identificadas: {secciones}\n")
        f.write(f"Párrafos convertidos: {parrafos}\n")
        f.write(f"Elementos de lista: {listas}\n\n")
        
        f.write("VENTAJAS DEL FORMATO MARKDOWN:\n")
        f.write("="*50 + "\n")
        f.write("1. ✅ Texto plano puro (sin formato binario)\n")
        f.write("2. ✅ Estructura clara con encabezados #, ##, ###\n")
        f.write("3. ✅ Listas fáciles de parsear (-, *, 1.)\n")
        f.write("4. ✅ Compatibilidad 100% con herramientas de texto\n")
        f.write("5. ✅ Tamaño reducido (mejor compresión)\n")
        f.write("6. ✅ Control de versiones perfecto con Git\n")
        f.write("7. ✅ Búsqueda instantánea (Ctrl+F, grep)\n")
        f.write("8. ✅ Edición rápida en cualquier editor\n")
        f.write("9. ✅ Conversión fácil a otros formatos (HTML, PDF, Word)\n")
        f.write("10.✅ Análisis automático más eficiente\n\n")
        
        f.write("ARCHIVOS CREADOS:\n")
        f.write("="*50 + "\n")
        f.write(f"1. {output_path} - Documento completo en Markdown\n")
        f.write(f"2. {output_simple} - Versión simplificada para análisis rápido\n")
        f.write(f"3. {indice_path} - Índice de contenido\n")
        f.write(f"4. {reporte_path} - Este reporte\n\n")
        
        f.write("PRÓXIMOS PASOS RECOMENDADOS:\n")
        f.write("="*50 + "\n")
        f.write("1. Usar el archivo Markdown para análisis futuro\n")
        f.write("2. Mantener sincronización con Word cuando sea necesario\n")
        f.write("3. Usar Git para control de versiones del Markdown\n")
        f.write("4. Crear scripts de conversión bidireccional Word↔Markdown\n")
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("CONVERSION A MARKDOWN COMPLETADA")
    print("="*60)
    print(f"Documento Word: {input_path}")
    print(f"Markdown completo: {output_path}")
    print(f"Markdown simplificado: {output_simple}")
    print(f"Índice: {indice_path}")
    print(f"Reporte: {reporte_path}")
    print(f"\nESTADÍSTICAS:")
    print(f"• Tamaño Word: {os.path.getsize(input_path):,} bytes")
    print(f"• Tamaño Markdown: {os.path.getsize(output_path):,} bytes")
    print(f"• Compresión: {os.path.getsize(output_path)/os.path.getsize(input_path)*100:.1f}%")
    print(f"• Secciones: {secciones}")
    print(f"• Párrafos: {parrafos}")
    print(f"• Elementos lista: {listas}")
    print("\n" + "="*60)
    print("VENTAJAS PARA ANALISIS FUTURO:")
    print("1. Analisis 5-10x mas rapido (texto plano vs binario)")
    print("2. Busqueda instantanea en todo el documento")
    print("3. Control de versiones perfecto con Git")
    print("4. Edicion rapida en cualquier editor")
    print("5. Conversion facil a otros formatos")
    print("="*60)
    
    return output_path

if __name__ == "__main__":
    convertir_word_a_markdown()