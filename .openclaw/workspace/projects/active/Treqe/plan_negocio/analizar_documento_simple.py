#!/usr/bin/env python3
"""
Analizar estructura del documento Word de Treqe
"""

import zipfile
import re

def analizar_documento():
    try:
        with zipfile.ZipFile('Plan_Negocio_Treqe_CON_SOLUCIONES_2026.docx', 'r') as docx:
            # Leer el documento principal
            with docx.open('word/document.xml') as f:
                content = f.read().decode('utf-8', errors='ignore')
            
            print('ANALISIS DEL DOCUMENTO TREQE')
            print('='*60)
            
            # Buscar secciones por patrones comunes
            patrones = [
                (r'<w:p[^>]*>.*?(PROPUESTA\s+DE\s+VALOR|VALOR\s+PROPUESTA).*?</w:p>', 'PROPUESTA DE VALOR'),
                (r'<w:p[^>]*>.*?(EXPERIENCIA\s+DE\s+USUARIO|USUARIO\s+EXPERIENCIA).*?</w:p>', 'EXPERIENCIA USUARIO'),
                (r'<w:p[^>]*>.*?(TECNOLOG[IÍ]A|ALGORITMO).*?</w:p>', 'TECNOLOGIA'),
                (r'<w:p[^>]*>.*?(GARANT[IÍ]A|SEGURO).*?</w:p>', 'GARANTIAS'),
                (r'<w:p[^>]*>.*?(SEGURIDAD|PROTECCION).*?</w:p>', 'SEGURIDAD'),
                (r'<w:p[^>]*>.*?(PROCESO|FLUJO).*?</w:p>', 'PROCESO'),
                (r'<w:p[^>]*>.*?(ENV[IÍ]O|LOG[IÍ]STICA).*?</w:p>', 'ENVIOS'),
                (r'<w:p[^>]*>.*?(SCORING|REPUTACION).*?</w:p>', 'SCORING'),
            ]
            
            encontradas = []
            for patron, nombre in patrones:
                matches = re.findall(patron, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    encontradas.append(nombre)
                    print(f'[OK] {nombre}: {len(matches)} ocurrencias')
            
            print(f'\\nSECCIONES ENCONTRADAS: {len(encontradas)}')
            print('Lista:', ', '.join(encontradas))
            
            # Buscar la seccion 8 (soluciones)
            if 'SECCIÓN 8' in content or 'Sección 8' in content or 'SECCION 8' in content:
                print('\\n[OK] SECCION 8 ENCONTRADA (Soluciones)')
            
            # Contar tamaño
            print(f'\\nTAMAÑO DEL DOCUMENTO: {len(content):,} caracteres')
            
            # Contar parrafos
            parrafos = content.count('<w:p ')
            print(f'PARRAFOS: {parrafos}')
            
            # Buscar donde termina el documento
            ultima_parte = content[-1000:] if len(content) > 1000 else content
            print('\\nULTIMAS 1000 CARACTERES:')
            print('-'*40)
            print(ultima_parte.replace('<', ' <').replace('>', '> ')[:500])
            
            return True
            
    except Exception as e:
        print(f'ERROR: {e}')
        return False

if __name__ == '__main__':
    analizar_documento()