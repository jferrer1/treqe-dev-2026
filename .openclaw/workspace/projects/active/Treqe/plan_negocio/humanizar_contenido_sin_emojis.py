#!/usr/bin/env python3
"""
Aplicar humanizer al contenido sin usar emojis (para Windows)
"""

import re
import random

def humanizar_texto_simple(texto):
    """Version simplificada de humanizer sin problemas de Unicode"""
    
    # Lista de cambios comunes
    cambios = [
        # Eliminar vocabulario AI
        (r'\bAdicionalmente\b', 'Tambien'),
        (r'\bprofundizar\b', 'analizar'),
        (r'\bintrincado\b', 'complejo'),
        (r'\bpivotal\b', 'importante'),
        (r'\bdestacar\b', 'señalar'),
        (r'\bsubrayar\b', 'indicar'),
        
        # Simplificar construcciones infladas
        (r'sirve como', 'es'),
        (r'se erige como', 'es'),
        (r'marca un hito', 'es importante'),
        (r'representa un', 'es un'),
        (r'cuenta con', 'tiene'),
        (r'ofrece', 'tiene'),
        
        # Eliminar analisis superficiales
        (r', destacando que', '. Esto muestra que'),
        (r', subrayando', '. Esto indica'),
        (r', enfatizando', '. Es importante que'),
        
        # Simplificar lenguaje promocional
        (r'vibrante', 'activa'),
        (r'rico', 'importante'),
        (r'profundo', 'significativo'),
        (r'innovador', 'nuevo'),
        (r'asombroso', 'notable'),
        
        # Eliminar atribuciones vagas
        (r'Informes del sector indican', 'Segun datos disponibles'),
        (r'Expertos argumentan', 'Algunos analistas dicen'),
        (r'Algunos criticos', 'Hay quien'),
        
        # Simplificar oraciones largas
        (r'(\w+), (\w+), y (\w+)', r'\1 y \2'),
        
        # Eliminar frases de relleno
        (r'con el fin de', 'para'),
        (r'debido al hecho de que', 'porque'),
        (r'en este momento', 'ahora'),
        (r'es importante señalar que', ''),
        (r'cabe destacar que', ''),
        
        # Reducir calificaciones excesivas
        (r'podria potencialmente', 'podria'),
        (r'quizas tenga algun efecto', 'puede afectar'),
        
        # Variaciones personales
        (r'El modelo se basa en', 'Creemos que el modelo funciona por'),
        (r'Los datos muestran que', 'Lo que vemos es que'),
        (r'El objetivo es', 'Queremos'),
        (r'La estrategia consiste en', 'Nuestro plan es'),
    ]
    
    for patron, reemplazo in cambios:
        texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
    
    # Dividir oraciones muy largas
    oraciones = texto.split('. ')
    nuevas_oraciones = []
    
    for oracion in oraciones:
        palabras = oracion.split()
        if len(palabras) > 30:
            # Encontrar punto natural para dividir
            mitad = len(palabras) // 2
            # Buscar conjuncion cerca de la mitad
            for i in range(mitad-5, mitad+5):
                if i < len(palabras) and palabras[i].lower() in ['y', 'pero', 'aunque', 'sin embargo', 'ademas']:
                    primera_parte = ' '.join(palabras[:i+1])
                    segunda_parte = ' '.join(palabras[i+1:])
                    nuevas_oraciones.append(primera_parte.strip() + '.')
                    nuevas_oraciones.append(segunda_parte.strip() + '.')
                    break
            else:
                # Dividir en la mitad si no hay conjuncion
                primera_parte = ' '.join(palabras[:mitad])
                segunda_parte = ' '.join(palabras[mitad:])
                nuevas_oraciones.append(primera_parte.strip() + '.')
                nuevas_oraciones.append(segunda_parte.strip() + '.')
        else:
            nuevas_oraciones.append(oracion.strip() + '.')
    
    texto = '. '.join(nuevas_oraciones)
    
    # Añadir algunas expresiones coloquiales
    expresiones = [
        'Dicho de otra forma',
        'En realidad',
        'Lo que pasa es que',
        'La verdad es que',
        'Si te fijas'
    ]
    
    # Añadir ocasionalmente
    if random.random() > 0.8:
        pos = texto.find('. ')
        if pos != -1:
            expresion = random.choice(expresiones)
            texto = texto[:pos+2] + expresion + ', ' + texto[pos+2:]
    
    return texto

def procesar_archivo(archivo_entrada, archivo_salida):
    """Procesar un archivo completo"""
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    lineas = contenido.split('\n')
    resultado = []
    
    for linea in lineas:
        if linea.startswith('#') or linea.startswith('##') or linea.startswith('###'):
            # Mantener titulos
            resultado.append(linea)
        elif linea.strip() == '':
            # Mantener lineas vacias
            resultado.append(linea)
        elif any(marker in linea for marker in ['**', '###', '---', '|']):
            # Mantener formato markdown especial
            resultado.append(linea)
        else:
            # Humanizar texto normal
            resultado.append(humanizar_texto_simple(linea))
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultado))
    
    return True

def main():
    print("Humanizando contenido sin emojis...")
    
    # Procesar modelo de negocio
    print("1. Humanizando modelo de negocio...")
    if procesar_archivo('seccion_modelo_negocio_mejorada.md', 'seccion_modelo_negocio_humanizada_final.md'):
        print("   OK: seccion_modelo_negocio_humanizada_final.md")
    
    # Procesar seccion legal
    print("2. Humanizando seccion legal...")
    if procesar_archivo('seccion_legal_mejorada.md', 'seccion_legal_humanizada_final.md'):
        print("   OK: seccion_legal_humanizada_final.md")
    
    print("\nHumanizacion completada.")
    print("Archivos creados:")
    print("- seccion_modelo_negocio_humanizada_final.md")
    print("- seccion_legal_humanizada_final.md")

if __name__ == '__main__':
    main()