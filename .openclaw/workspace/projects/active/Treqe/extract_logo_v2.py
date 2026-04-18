#!/usr/bin/env python3
"""
Extrae el texto "treqe" con bordes suaves, eliminando fondo y etiquetas.
Usa técnicas avanzadas para preservar anti-aliasing.
"""

import sys
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

def extract_text_with_smooth_edges(input_path, output_path):
    """Extrae texto manteniendo bordes suaves y eliminando halo."""
    print("Cargando imagen...")
    img = Image.open(input_path)
    img = img.convert("RGBA")
    
    width, height = img.size
    print(f"Dimensiones: {width}x{height}")
    
    # Convertir a numpy
    data = np.array(img, dtype=np.float32) / 255.0
    
    # Separar canales
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # El texto es azul oscuro: bajo R, medio-bajo G, alto B
    # Fondo es salmón: alto R, medio G, medio B
    # Calcular diferencia de color para identificar texto
    
    # Método 1: Diferencia entre canal B y promedio de R+G
    # El azul tiene B mucho mayor que R y G
    blue_strength = b - (r + g) / 2.0
    
    # Método 2: Distancia al color azul objetivo (0, 35, 78) en RGB 0-255
    target_blue = np.array([0, 35, 78]) / 255.0
    target_dist = np.sqrt((r - target_blue[0])**2 + 
                         (g - target_blue[1])**2 + 
                         (b - target_blue[2])**2)
    
    # Método 3: Distancia al color salmón objetivo (255, 183, 178)
    target_salmon = np.array([255, 183, 178]) / 255.0
    salmon_dist = np.sqrt((r - target_salmon[0])**2 +
                         (g - target_salmon[1])**2 +
                         (b - target_salmon[2])**2)
    
    # Combinar métricas: texto donde blue_strength es alto Y target_dist es bajo
    text_score = (blue_strength + 1.0) / 2.0  # Normalizar 0-1
    text_score = text_score * (1.0 - target_dist)  # Multiplicar por inversa de distancia
    
    # Suavizar score para bordes más limpios
    from scipy.ndimage import gaussian_filter
    text_score_smooth = gaussian_filter(text_score, sigma=1.0)
    
    # Umbral adaptativo: usar percentil
    threshold = np.percentile(text_score_smooth[text_score_smooth > 0.1], 70)
    if threshold < 0.3:
        threshold = 0.3
    
    # Crear máscara suave (alpha)
    alpha_mask = np.clip((text_score_smooth - threshold) / (1 - threshold), 0, 1)
    
    # Identificar etiquetas negras (todos canales bajos)
    black_mask = (r < 0.2) & (g < 0.2) & (b < 0.2) & (text_score_smooth < threshold)
    
    # Identificar fondo salmón (distancia baja al color salmón)
    salmon_mask = salmon_dist < 0.2
    
    # Eliminar etiquetas y fondo de la máscara
    alpha_mask[black_mask] = 0
    alpha_mask[salmon_mask] = 0
    
    # Crear nueva imagen
    new_data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Color del texto (azul original)
    text_color_r = np.uint8(r * 255)
    text_color_g = np.uint8(g * 255) 
    text_color_b = np.uint8(b * 255)
    
    # Aplicar máscara alpha
    alpha_uint8 = np.uint8(alpha_mask * 255)
    
    new_data[:,:,0] = text_color_r
    new_data[:,:,1] = text_color_g
    new_data[:,:,2] = text_color_b
    new_data[:,:,3] = alpha_uint8
    
    # Crear imagen PIL
    result_img = Image.fromarray(new_data, 'RGBA')
    
    # Aplicar filtro de suavizado ligero en bordes
    result_img = result_img.filter(ImageFilter.SMOOTH_MORE)
    
    # Recortar espacio transparente
    alpha_np = np.array(result_img.getchannel('A'))
    non_zero = np.where(alpha_np > 10)
    
    if len(non_zero[0]) > 0:
        y_min, y_max = np.min(non_zero[0]), np.max(non_zero[0])
        x_min, x_max = np.min(non_zero[1]), np.max(non_zero[1])
        
        margin = 8
        y_min = max(0, y_min - margin)
        y_max = min(height - 1, y_max + margin)
        x_min = max(0, x_min - margin)
        x_max = min(width - 1, x_max + margin)
        
        result_img = result_img.crop((x_min, y_min, x_max, y_max))
        print(f"Recortado a: {x_max-x_min}x{y_max-y_min}")
    
    # Guardar
    result_img.save(output_path, 'PNG', compress_level=9)
    print(f"Imagen guardada: {output_path}")
    
    # Crear también versión SVG vectorial (texto simple)
    # Para logo de texto, SVG sería ideal
    create_svg_version(output_path, result_img)
    
    return True

def create_svg_version(png_path, pil_image):
    """Crea una versión SVG aproximada del logo."""
    svg_path = str(png_path).replace('.png', '.svg')
    
    # Dimensiones
    width, height = pil_image.size
    
    # SVG simple: rectángulo con texto (aproximación)
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');
      .treqe-text {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: {height * 0.7}px;
        fill: #00234E;
        letter-spacing: -0.07em;
      }}
    </style>
  </defs>
  <text x="50%" y="60%" text-anchor="middle" class="treqe-text">treqe</text>
</svg>'''
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"SVG creado: {svg_path}")
    return svg_path

if __name__ == "__main__":
    input_path = Path(r"C:\Users\Shadow\.openclaw\media\inbound\74c907b6-3193-48c7-9ad6-3407922f47af.png")
    
    if not input_path.exists():
        print(f"ERROR: No se encuentra la imagen: {input_path}")
        sys.exit(1)
    
    output_path = Path(r"C:\Users\Shadow\.openclaw\workspace\projects\active\Treqe\logo-treqe-extracted-v2.png")
    
    try:
        success = extract_text_with_smooth_edges(str(input_path), str(output_path))
        if success:
            print("EXTRACCION COMPLETADA")
            print(f"Archivo: {output_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)