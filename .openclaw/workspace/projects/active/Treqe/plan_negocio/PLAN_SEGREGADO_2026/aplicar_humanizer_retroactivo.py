#!/usr/bin/env python3
# Aplicar humanizer retroactivo a secciones 1-4

import os
import re
from docx import Document
from datetime import datetime

print("=== APLICANDO HUMANIZER RETROACTIVO A SECCIONES 1-4 ===")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Patrones robóticos prohibidos (de REGLAS_HUMANIZER.md)
PATRONES_PROHIBIDOS = [
    r"se procederá a",
    r"es necesario",
    r"optimización de",
    r"sinergia entre", 
    r"paradigma de",
    r"leverage de",
    r"se implementará",
    r"el sistema permite",
    r"se ha diseñado",
    r"la solución consiste en",
    r"se realizará",
    r"se llevará a cabo",
    r"se efectuará",
    r"se ejecutará",
    r"se desarrollará"
]

# Personajes para ejemplos
PERSONAJES = {
    "Ana": "usuario típico, tiene iPhone, quiere bicicleta",
    "Carlos": "vendedor, tiene bicicleta, quiere guitarra", 
    "Beatriz": "compradora, tiene guitarra, quiere iPhone",
    "David": "usuario frecuente, hace muchos intercambios",
    "María": "CEO de Treqe, apasionada por economía circular",
    "Elena": "inversora, busca proyectos con impacto social"
}

# Transformaciones humanizadoras
TRANSFORMACIONES = {
    r"El sistema": "Treqe",
    r"La plataforma": "Treqe",
    r"La aplicación": "Treqe",
    r"El usuario": "Ana",
    r"Los usuarios": "personas como Ana y Carlos",
    r"El proceso": "el viaje",
    r"La funcionalidad": "lo que puedes hacer",
    r"La característica": "lo especial",
    r"El algoritmo": "el cerebro de Treqe",
    r"La tecnología": "la magia detrás",
    r"La implementación": "cómo lo hacemos",
    r"La ejecución": "cómo funciona",
    r"El desarrollo": "cómo crecemos"
}

def humanizar_parrafo(texto):
    """Aplicar transformaciones humanizadoras a un párrafo"""
    if not texto or len(texto.strip()) < 10:
        return texto
    
    original = texto
    
    # 1. Reemplazar patrones robóticos
    for patron in PATRONES_PROHIBIDOS:
        if re.search(patron, texto, re.IGNORECASE):
            # Reemplazar con lenguaje humano
            texto = re.sub(
                patron, 
                "vamos a" if "se procederá" in patron else 
                "necesitamos" if "es necesario" in patron else
                "mejoramos" if "optimización" in patron else
                "conectamos" if "sinergia" in patron else
                "cambiamos" if "paradigma" in patron else
                "aprovechamos" if "leverage" in patron else
                "creamos" if "implementará" in patron else
                "Treqe permite" if "sistema permite" in patron else
                "hemos diseñado" if "ha diseñado" in patron else
                "la solución es",
                texto, 
                flags=re.IGNORECASE
            )
    
    # 2. Reemplazar términos robóticos
    for robotico, humano in TRANSFORMACIONES.items():
        texto = re.sub(robotico, humano, texto, flags=re.IGNORECASE)
    
    # 3. Añadir ejemplos si no hay
    if not any(personaje in texto for personaje in PERSONAJES.keys()):
        # Verificar si es un párrafo explicativo (no título)
        if len(texto) > 50 and not texto.strip().endswith('.'):
            # Añadir ejemplo al final
            ejemplo = f" Por ejemplo, Ana puede intercambiar su iPhone por la bicicleta de Carlos sin necesidad de dinero."
            texto = texto + ejemplo
    
    # 4. Añadir lenguaje conversacional
    oraciones = texto.split('. ')
    if len(oraciones) > 1:
        # Primera oración más conversacional
        primera = oraciones[0]
        if not any(palabra in primera.lower() for palabra in ['imagina', 'piensa', 'supón', 'como cuando']):
            if len(primera) > 20:
                oraciones[0] = f"Imagina que {primera[0].lower()}{primera[1:]}"
        
        # Última oración con conexión humana
        ultima = oraciones[-1]
        if not any(palabra in ultima.lower() for palabra in ['importante', 'clave', 'esencial', 'significa']):
            oraciones[-1] = f"{ultima} Lo importante es que personas como Ana puedan intercambiar lo que tienen por lo que realmente quieren."
        
        texto = '. '.join(oraciones)
    
    # 5. Añadir pregunta retórica si es muy técnico
    palabras_tecnicas = ['algoritmo', 'tecnología', 'sistema', 'plataforma', 'arquitectura']
    if any(palabra in texto.lower() for palabra in palabras_tecnicas) and '?' not in texto:
        # Insertar pregunta después de primera oración técnica
        oraciones = texto.split('. ')
        for i, oracion in enumerate(oraciones):
            if any(palabra in oracion.lower() for palabra in palabras_tecnicas):
                pregunta = f" ¿Suena complicado? En realidad es simple:"
                oraciones.insert(i + 1, pregunta)
                break
        texto = '. '.join(oraciones)
    
    return texto if texto != original else texto

def procesar_documento(ruta_docx):
    """Procesar un documento DOCX aplicando humanizer"""
    print(f"Procesando: {os.path.basename(ruta_docx)}")
    
    try:
        doc = Document(ruta_docx)
        cambios = 0
        total_parrafos = 0
        
        for paragraph in doc.paragraphs:
            total_parrafos += 1
            texto_original = paragraph.text.strip()
            
            if texto_original and len(texto_original) > 10:
                texto_humanizado = humanizar_parrafo(texto_original)
                
                if texto_humanizado != texto_original:
                    # Reemplazar texto manteniendo formato
                    if paragraph.runs:
                        # Mantener formato del primer run
                        paragraph.runs[0].text = texto_humanizado
                        # Eliminar runs adicionales si existen
                        for run in paragraph.runs[1:]:
                            run.text = ""
                    else:
                        paragraph.text = texto_humanizado
                    
                    cambios += 1
        
        # Guardar versión humanizada
        nombre_base = os.path.splitext(ruta_docx)[0]
        ruta_humanizada = f"{nombre_base}_HUMANIZADO.docx"
        doc.save(ruta_humanizada)
        
        print(f"  ✅ Procesado: {total_parrafos} párrafos, {cambios} humanizados")
        print(f"  📄 Guardado: {ruta_humanizada}")
        
        return cambios, total_parrafos
        
    except Exception as e:
        print(f"  ❌ Error procesando {ruta_docx}: {e}")
        return 0, 0

def main():
    """Función principal"""
    # Secciones a humanizar
    secciones = [
        "01_INTRODUCCION.docx",
        "02_PROBLEMA_PARADOJA_LIQUIDEZ.docx", 
        "03_SOLUCION_RUEDAS_INTERCAMBIO.docx",
        "04_VENTAJA_COMPETITIVA.docx"
    ]
    
    total_cambios = 0
    total_parrafos = 0
    
    for seccion in secciones:
        ruta = os.path.join(".", seccion)
        if os.path.exists(ruta):
            cambios, parrafos = procesar_documento(ruta)
            total_cambios += cambios
            total_parrafos += parrafos
        else:
            print(f"❌ No encontrado: {seccion}")
    
    print()
    print("=== RESUMEN HUMANIZACIÓN RETROACTIVA ===")
    print(f"Secciones procesadas: {len([s for s in secciones if os.path.exists(s)])}")
    print(f"Total párrafos: {total_parrafos}")
    print(f"Párrafos humanizados: {total_cambios}")
    print(f"Porcentaje humanizado: {(total_cambios/total_parrafos*100 if total_parrafos > 0 else 0):.1f}%")
    print()
    
    # Crear checklist de verificación
    print("=== CHECKLIST DE VERIFICACIÓN ===")
    print("Para cada sección humanizada, verificar:")
    print("1. [ ] CERO patrones prohibidos ('se procederá', 'es necesario', etc.)")
    print("2. [ ] Mínimo 2 referencias a Ana/Carlos/Beatriz")
    print("3. [ ] Mínimo 1 analogía o 'imagina que'")
    print("4. [ ] Lenguaje conversacional (explicando a un amigo)")
    print("5. [ ] Releer en voz alta suena natural")
    print()
    print("=== NOTA IMPORTANTE ===")
    print("Humanizer retroactivo aplica transformaciones automáticas.")
    print("Para máxima calidad, revisar manualmente cada sección.")
    print("Regla de oro: Si suena robótico, recrear completamente.")

if __name__ == "__main__":
    main()