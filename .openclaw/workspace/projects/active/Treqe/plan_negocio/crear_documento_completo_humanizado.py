#!/usr/bin/env python3
"""
Crear documento Markdown completo con secciones humanizadas
"""

import re

def leer_archivo(ruta):
    """Leer archivo con encoding correcto"""
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()

def guardar_archivo(ruta, contenido):
    """Guardar archivo con encoding correcto"""
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)

def crear_documento_completo():
    print("Creando documento Markdown completo humanizado...")
    
    # 1. Leer documento original en Markdown
    original = leer_archivo('Plan_Negocio_Treqe_TRABAJO.md')
    print(f"Documento original: {len(original)} caracteres")
    
    # 2. Leer secciones humanizadas
    modelo_humanizado = leer_archivo('modelo_negocio_humanizado_final.md')
    marketing_humanizado = leer_archivo('marketing_humanizado_final.md')
    
    print(f"Modelo humanizado: {len(modelo_humanizado)} caracteres")
    print(f"Marketing humanizado: {len(marketing_humanizado)} caracteres")
    
    # 3. Dividir documento original por secciones
    # Buscar sección 5
    patron_seccion5 = r'(# 5\..*?)(?=# 6\.|$)'
    match5 = re.search(patron_seccion5, original, re.DOTALL)
    
    if match5:
        seccion5_original = match5.group(1)
        print(f"Sección 5 original encontrada: {len(seccion5_original)} caracteres")
        
        # Reemplazar sección 5
        original = original.replace(seccion5_original, modelo_humanizado)
        print("✅ Sección 5 reemplazada")
    else:
        print("⚠️ Sección 5 no encontrada, insertando al final de sección 4")
        # Buscar fin de sección 4
        patron_fin_seccion4 = r'(# 4\..*?)(?=# 5\.|$)'
        match4 = re.search(patron_fin_seccion4, original, re.DOTALL)
        if match4:
            # Insertar después de sección 4
            posicion = match4.end()
            original = original[:posicion] + '\n\n' + modelo_humanizado + '\n\n' + original[posicion:]
            print("✅ Sección 5 insertada después de sección 4")
    
    # 4. Buscar sección 10
    patron_seccion10 = r'(# 10\..*?)(?=# 11\.|$)'
    match10 = re.search(patron_seccion10, original, re.DOTALL)
    
    if match10:
        seccion10_original = match10.group(1)
        print(f"Sección 10 original encontrada: {len(seccion10_original)} caracteres")
        
        # Reemplazar sección 10
        original = original.replace(seccion10_original, marketing_humanizado)
        print("✅ Sección 10 reemplazada")
    else:
        print("⚠️ Sección 10 no encontrada, buscando 'MARKETING'")
        # Buscar por texto
        lineas = original.split('\n')
        for i, linea in enumerate(lineas):
            if 'MARKETING' in linea.upper():
                print(f"Encontrado 'MARKETING' en línea {i}: {linea[:50]}...")
                # Insertar después de esta línea
                lineas.insert(i + 1, '\n' + marketing_humanizado)
                original = '\n'.join(lineas)
                print("✅ Sección 10 insertada")
                break
    
    # 5. Guardar documento completo
    output_path = 'Plan_Negocio_Treqe_COMPLETO_HUMANIZADO.md'
    guardar_archivo(output_path, original)
    
    print(f"\n✅ DOCUMENTO COMPLETO CREADO: {output_path}")
    print(f"✅ Tamaño final: {len(original)} caracteres")
    
    # 6. Crear también versión con solo secciones humanizadas (para revisión)
    crear_version_revision(modelo_humanizado, marketing_humanizado)
    
    return output_path

def crear_version_revision(modelo, marketing):
    """Crear versión solo con secciones humanizadas para revisión fácil"""
    
    contenido = """# TREQE - SECCIONES HUMANIZADAS PARA REVISIÓN

**Fecha:** 26 de febrero 2026
**Estado:** Versión humanizada lista para revisión
**Formato:** Markdown (fácil de leer y editar)

---

## SECCIÓN 5: MODELO DE NEGOCIO (HUMANIZADO)

"""

    contenido += modelo
    contenido += "\n\n---\n\n"
    contenido += "## SECCIÓN 10: MARKETING (HUMANIZADO)\n\n"
    contenido += marketing
    
    contenido += """

---

## 📋 INSTRUCCIONES DE REVISIÓN:

1. **Lee cada sección** y verifica que el tono sea humano, no corporativo
2. **Busca lenguaje técnico** que pueda simplificarse
3. **Verifica que haya opiniones** ("creemos", "pensamos", "probablemente")
4. **Asegúrate de que sea honesto** sobre lo que no sabemos
5. **El tono debe ser** conversacional, no de presentación corporativa

## 🎯 QUÉ BUSCAMOS:

- ✅ **Lenguaje natural**, no corporativo
- ✅ **Opiniones personales**, no solo datos
- ✅ **Reconocimiento de incertidumbre**
- ✅ **Historias y ejemplos**, no solo listas
- ✅ **Tono conversacional**, como si lo explicara una persona

## 🔄 PRÓXIMOS PASOS:

1. **Revisar estas secciones**
2. **Dar feedback** sobre qué mejorar
3. **Humanizar otras secciones** (legal, anexos, etc.)
4. **Convertir a Word** cuando todo esté 100% terminado
"""

    revision_path = 'Treqe_SECCIONES_HUMANIZADAS_REVISION.md'
    guardar_archivo(revision_path, contenido)
    
    print(f"✅ VERSIÓN DE REVISIÓN: {revision_path}")
    print(f"✅ Tamaño: {len(contenido)} caracteres")

if __name__ == '__main__':
    crear_documento_completo()