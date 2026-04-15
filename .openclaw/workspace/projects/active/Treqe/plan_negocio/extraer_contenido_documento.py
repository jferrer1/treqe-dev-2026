#!/usr/bin/env python3
"""
Extraer contenido legible del documento Word para analizar su estructura
"""

import zipfile
import re
from xml.etree import ElementTree as ET

def extraer_texto_legible():
    """Extraer texto legible del documento Word"""
    try:
        with zipfile.ZipFile('Plan_Negocio_Treqe_CON_SOLUCIONES_2026.docx', 'r') as docx:
            # Leer el documento principal
            with docx.open('word/document.xml') as f:
                content = f.read()
            
            # Parsear XML
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
            }
            
            root = ET.fromstring(content)
            
            # Extraer todo el texto
            text_parts = []
            
            # Buscar todos los elementos de texto
            for elem in root.iter():
                if elem.tag.endswith('}t'):  # Elementos de texto
                    if elem.text:
                        text_parts.append(elem.text)
                elif elem.tag.endswith('}p'):  # Párrafos
                    # Añadir salto de línea después de cada párrafo
                    text_parts.append('\n')
            
            texto_completo = ''.join(text_parts)
            
            # Limpiar y organizar
            texto_completo = re.sub(r'\n\s*\n+', '\n\n', texto_completo)  # Limpiar múltiples saltos
            texto_completo = texto_completo.strip()
            
            # Guardar para análisis
            with open('contenido_documento_original.txt', 'w', encoding='utf-8') as f:
                f.write(texto_completo)
            
            print(f"Texto extraído: {len(texto_completo)} caracteres")
            print(f"Guardado en: contenido_documento_original.txt")
            
            # Buscar secciones específicas
            secciones_buscar = [
                'envío', 'envios', 'logística', 'recepcion',
                'garantía', 'garantias', 'seguro',
                'scoring', 'reputación', 'puntuación',
                'proceso', 'flujo', 'usuario elige',
                'selecciona', 'preferencias'
            ]
            
            print("\nBUSCANDO SECCIONES RELEVANTES:")
            print("="*60)
            
            lineas = texto_completo.split('\n')
            for i, linea in enumerate(lineas):
                linea_lower = linea.lower()
                for palabra in secciones_buscar:
                    if palabra in linea_lower and len(linea.strip()) > 10:
                        # Mostrar contexto
                        print(f"\nLínea {i+1}: {linea.strip()}")
                        # Mostrar las siguientes 3 líneas
                        for j in range(1, 4):
                            if i+j < len(lineas):
                                print(f"  + {lineas[i+j].strip()}")
                        break
            
            return texto_completo
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    extraer_texto_legible()