#!/usr/bin/env python3
"""
Extrae el texto "treqe" de la imagen, eliminando fondo y etiquetas.
Guarda como PNG con transparencia.
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

def extract_text_from_image(input_path, output_path):
    """Extrae texto azul oscuro de fondo salmón, guarda con transparencia."""
    print(f"Cargando imagen: {input_path}")
    img = Image.open(input_path)
    img = img.convert("RGBA")  # Asegurar canal alfa
    
    width, height = img.size
    print(f"Dimensiones: {width}x{height}")
    
    # Convertir a numpy para procesamiento
    data = np.array(img)
    
    # Definir colores de referencia (obtenidos del análisis)
    # Fondo salmón: RGB ~(255, 183, 178) 
    # Texto azul: RGB ~(0, 35, 78) o similar
    # Etiquetas negras: RGB ~(0, 0, 0)
    
    # Separar canales
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Crear máscara para el texto azul
    # El texto azul tiene R muy bajo, G medio-bajo, B alto
    blue_mask = (r < 50) & (g < 100) & (b > 30) & (r < g) & (g < b)
    
    # También podemos identificar el fondo salmón (alto R, medio G, medio B)
    salmon_mask = (r > 200) & (g > 150) & (g < 200) & (b > 150) & (b < 200)
    
    # Identificar etiquetas negras (todas bajas)
    black_mask = (r < 50) & (g < 50) & (b < 50) & ~blue_mask
    
    print(f"Píxeles texto azul: {np.sum(blue_mask)}")
    print(f"Píxeles fondo salmón: {np.sum(salmon_mask)}")
    print(f"Píxeles etiquetas negras: {np.sum(black_mask)}")
    
    # Crear nueva imagen con transparencia
    new_data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Mantener el texto azul como color original
    new_data[blue_mask] = data[blue_mask]
    
    # Para píxeles de texto, mantener opacidad completa
    new_data[blue_mask, 3] = 255  # Alpha completo
    
    # Para píxeles de fondo, hacer transparentes
    new_data[salmon_mask, 3] = 0  # Completamente transparente
    
    # Para píxeles de etiquetas negras, también transparentes
    new_data[black_mask, 3] = 0
    
    # Para píxeles restantes (bordes, anti-aliasing), usar transparencia basada en distancia
    # Simplemente haremos transparentes todos los no-texto
    remaining_mask = ~blue_mask & ~salmon_mask & ~black_mask
    new_data[remaining_mask, 3] = 0
    
    # Opcional: suavizar bordes del texto (preservar anti-aliasing)
    # Para simplificar, mantendremos los valores originales de alpha donde haya texto
    
    # Crear imagen final
    result_img = Image.fromarray(new_data, 'RGBA')
    
    # Recortar espacio blanco (transparente) alrededor
    # Primero encontramos bounding box del texto no transparente
    alpha_channel = new_data[:,:,3]
    non_transparent = np.where(alpha_channel > 0)
    
    if len(non_transparent[0]) > 0:
        y_min, y_max = np.min(non_transparent[0]), np.max(non_transparent[0])
        x_min, x_max = np.min(non_transparent[1]), np.max(non_transparent[1])
        
        # Añadir pequeño margen
        margin = 5
        y_min = max(0, y_min - margin)
        y_max = min(height - 1, y_max + margin)
        x_min = max(0, x_min - margin)
        x_max = min(width - 1, x_max + margin)
        
        result_img = result_img.crop((x_min, y_min, x_max, y_max))
        print(f"Recortado a: {x_max-x_min}x{y_max-y_min}")
    
    # Guardar
    result_img.save(output_path, 'PNG')
    print(f"Imagen guardada: {output_path}")
    print(f"Tamaño: {result_img.size}")
    
    return True

if __name__ == "__main__":
    # Ruta de entrada (imagen adjunta)
    input_path = Path(r"C:\Users\Shadow\.openclaw\media\inbound\74c907b6-3193-48c7-9ad6-3407922f47af.png")
    
    if not input_path.exists():
        print(f"ERROR: No se encuentra la imagen: {input_path}")
        sys.exit(1)
    
    # Ruta de salida en proyecto Treqe
    output_path = Path(r"C:\Users\Shadow\.openclaw\workspace\projects\active\Treqe\logo-treqe-extracted.png")
    
    try:
        success = extract_text_from_image(str(input_path), str(output_path))
        if success:
            print("✅ Extracción completada exitosamente")
            print(f"📁 Archivo: {output_path}")
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)