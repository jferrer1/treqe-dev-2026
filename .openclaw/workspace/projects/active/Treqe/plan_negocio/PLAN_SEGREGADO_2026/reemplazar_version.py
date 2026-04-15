#!/usr/bin/env python3
import os
import time

print("Reemplazando versiones...")

# Esperar un momento para que se libere el archivo
time.sleep(2)

# Verificar archivos
if os.path.exists("06_PROYECCIONES_FINANCIERAS_HUMANIZADO.docx"):
    print("Archivo humanizado encontrado: 06_PROYECCIONES_FINANCIERAS_HUMANIZADO.docx")
    
    # Eliminar versión anterior si existe
    if os.path.exists("06_PROYECCIONES_FINANCIERAS.docx"):
        try:
            os.remove("06_PROYECCIONES_FINANCIERAS.docx")
            print("Versión anterior eliminada")
        except:
            print("No se pudo eliminar versión anterior (puede estar abierta)")
            # Crear nombre alternativo
            backup_name = "06_PROYECCIONES_FINANCIERAS_ANTERIOR.docx"
            os.rename("06_PROYECCIONES_FINANCIERAS.docx", backup_name)
            print(f"Versión anterior renombrada a: {backup_name}")
    
    # Renombrar humanizado a nombre estándar
    os.rename("06_PROYECCIONES_FINANCIERAS_HUMANIZADO.docx", "06_PROYECCIONES_FINANCIERAS.docx")
    
    tamaño = os.path.getsize("06_PROYECCIONES_FINANCIERAS.docx")
    print(f"✅ VERSIÓN HUMANIZADA INSTALADA: 06_PROYECCIONES_FINANCIERAS.docx ({tamaño:,} bytes)")
    
    # Verificar contenido humanizado
    from docx import Document
    doc = Document("06_PROYECCIONES_FINANCIERAS.docx")
    texto = ' '.join([p.text for p in doc.paragraphs])
    
    print("\nVERIFICACIÓN HUMANIZER:")
    print(f"- Ejemplos 'Ana': {texto.lower().count('ana')}")
    print(f"- Ejemplos 'Carlos': {texto.lower().count('carlos')}")
    print(f"- Ejemplos 'Beatriz': {texto.lower().count('beatriz')}")
    print(f"- Patrón 'se procederá': {'NO' if 'se procederá' not in texto.lower() else 'SÍ (ERROR)'}")
    print(f"- Patrón 'es necesario': {'NO' if 'es necesario' not in texto.lower() else 'SÍ (ERROR)'}")
    print(f"- Patrón 'optimización': {'NO' if 'optimización' not in texto.lower() else 'SÍ (ERROR)'}")
    
else:
    print("ERROR: No se encontró archivo humanizado")