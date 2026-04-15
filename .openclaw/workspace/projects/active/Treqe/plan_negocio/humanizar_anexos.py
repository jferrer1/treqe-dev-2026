#!/usr/bin/env python3
"""
Humanizar los anexos
"""

import re

def humanizar_texto(texto):
    """Version simplificada para anexos"""
    
    cambios = [
        # Vocabulario AI
        (r'\bAdicionalmente\b', 'Tambien'),
        (r'\bprofundizar\b', 'analizar'),
        (r'\bintrincado\b', 'complejo'),
        (r'\bclave\b', 'importante'),
        (r'\bpaisaje\b', 'sector'),
        (r'\btapiz\b', 'conjunto'),
        
        # Construcciones infladas
        (r'sirve como', 'es'),
        (r'se erige como', 'es'),
        (r'cuenta con', 'tiene'),
        (r'ofrece', 'tiene'),
        
        # Lenguaje promocional
        (r'vibrante', 'activa'),
        (r'rico', 'importante'),
        (r'innovador', 'nuevo'),
        (r'asombroso', 'notable'),
        
        # Atribuciones vagas
        (r'Informes del sector', 'Datos disponibles'),
        (r'Expertos argumentan', 'Algunos analistas dicen'),
        
        # Frases de relleno
        (r'con el fin de', 'para'),
        (r'es importante señalar que', ''),
        (r'cabe destacar que', ''),
        
        # Personalizar
        (r'El modelo se basa en', 'Creemos que el modelo funciona por'),
        (r'Los datos muestran que', 'Lo que vemos es que'),
    ]
    
    for patron, reemplazo in cambios:
        texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
    
    # Dividir oraciones largas
    oraciones = texto.split('. ')
    nuevas = []
    
    for oracion in oraciones:
        palabras = oracion.split()
        if len(palabras) > 25:
            mitad = len(palabras) // 2
            primera = ' '.join(palabras[:mitad])
            segunda = ' '.join(palabras[mitad:])
            nuevas.append(primera.strip() + '.')
            nuevas.append(segunda.strip() + '.')
        else:
            nuevas.append(oracion.strip() + '.')
    
    return '. '.join(nuevas)

def main():
    with open('anexos_completos.md', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    lineas = contenido.split('\n')
    resultado = []
    
    for linea in lineas:
        if linea.startswith('#') or linea.startswith('##') or linea.startswith('###'):
            resultado.append(linea)
        elif linea.strip() == '':
            resultado.append(linea)
        elif '|' in linea or '---' in linea or '**' in linea:
            resultado.append(linea)
        else:
            resultado.append(humanizar_texto(linea))
    
    with open('anexos_humanizados_final.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultado))
    
    print("Anexos humanizados guardados en: anexos_humanizados_final.md")

if __name__ == '__main__':
    main()