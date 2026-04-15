#!/usr/bin/env python3
"""
Crear documentos sin caracteres Unicode para evitar errores
"""

import re

def leer(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()

def guardar(ruta, contenido):
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)

def main():
    print("Creando documentos sin Unicode...")
    
    # Leer contenido
    original = leer('Plan_Negocio_Treqe_TRABAJO.md')
    modelo = leer('modelo_negocio_humanizado_final.md')
    marketing = leer('marketing_humanizado_final.md')
    
    print(f"Original: {len(original)} chars")
    print(f"Modelo: {len(modelo)} chars")
    print(f"Marketing: {len(marketing)} chars")
    
    # 1. Documento completo con secciones humanizadas
    # Reemplazar sección 5
    seccion5_match = re.search(r'(# 5\..*?)(?=# 6\.|$)', original, re.DOTALL)
    if seccion5_match:
        original = original.replace(seccion5_match.group(1), modelo)
        print("Seccion 5 reemplazada")
    
    # Reemplazar sección 10
    seccion10_match = re.search(r'(# 10\..*?)(?=# 11\.|$)', original, re.DOTALL)
    if seccion10_match:
        original = original.replace(seccion10_match.group(1), marketing)
        print("Seccion 10 reemplazada")
    
    guardar('Plan_Negocio_Treqe_COMPLETO_HUMANIZADO.md', original)
    print("Documento completo guardado")
    
    # 2. Versión solo para revisión
    revision = f"""# TREQE - SECCIONES HUMANIZADAS PARA REVISIÓN

Fecha: 26 de febrero 2026
Estado: Versión humanizada lista para revisión
Formato: Markdown (facil de leer y editar)

---

## SECCION 5: MODELO DE NEGOCIO (HUMANIZADO)

{modelo}

---

## SECCION 10: MARKETING (HUMANIZADO)

{marketing}

---

## INSTRUCCIONES DE REVISION:

1. Lee cada seccion y verifica que el tono sea humano, no corporativo
2. Busca lenguaje tecnico que pueda simplificarse
3. Verifica que haya opiniones ("creemos", "pensamos", "probablemente")
4. Asegurate de que sea honesto sobre lo que no sabemos
5. El tono debe ser conversacional, no de presentacion corporativa

## QUE BUSCAMOS:

- Lenguaje natural, no corporativo
- Opiniones personales, no solo datos
- Reconocimiento de incertidumbre
- Historias y ejemplos, no solo listas
- Tono conversacional, como si lo explicara una persona

## PROXIMOS PASOS:

1. Revisar estas secciones
2. Dar feedback sobre que mejorar
3. Humanizar otras secciones (legal, anexos, etc.)
4. Convertir a Word cuando todo este 100% terminado
"""
    
    guardar('Treqe_SECCIONES_HUMANIZADAS_REVISION.md', revision)
    print("Version de revision guardada")
    
    # 3. También crear un archivo pequeño con solo las mejoras
    mejoras = f"""# TREQE - MEJORAS APLICADAS (26 febrero 2026)

## QUE SE HA HUMANIZADO:

### 1. SECCION 5: MODELO DE NEGOCIO
- **Antes:** Lenguaje corporativo, estructura formal, sin personalidad
- **Ahora:** Tono conversacional, ejemplos reales, opiniones personales
- **Cambio clave:** De "optimizamos flujos de ingresos" a "cobramos sin que duela"

### 2. SECCION 10: MARKETING
- **Antes:** Estrategia generica, checkmarks, lenguaje de marketing
- **Ahora:** Enfoque practico, crecimiento organico, honestidad sobre limites
- **Cambio clave:** De "canales de adquisicion multicapa" a "empezamos con 50 personas que conocemos"

## EJEMPLOS DE HUMANIZACION:

### ANTES (corporativo):
"El modelo de negocio de Treqe se fundamenta en una estructura de comisiones escalonadas que optimiza la captura de valor mientras garantiza la sostenibilidad economica del ecosistema."

### AHORA (humano):
"Cobramos un pequeno porcentaje cuando un intercambio funciona. No antes. Si falla, no cobramos nada. Menos de 100€: 1.5% (un cafe, basicamente)."

### ANTES (marketing generico):
"Implementaremos una estrategia multicanal integrando SEO, marketing de contenidos y publicidad segmentada para maximizar la adquisicion de usuarios."

### AHORA (marketing humano):
"No empezamos con anuncios. Empezamos con 50 personas. Personas reales que conocemos. Les decimos: 'Prueba esto. Si te gusta, cuentaselo a un amigo.'"

## ESTADO ACTUAL:
- [x] Seccion 5 humanizada (modelo de negocio)
- [x] Seccion 10 humanizada (marketing)
- [ ] Seccion 11 por humanizar (legal)
- [ ] Anexos por humanizar
- [ ] Otras secciones por revisar

## ARCHIVOS CREADOS:
1. Plan_Negocio_Treqe_COMPLETO_HUMANIZADO.md - Documento completo
2. Treqe_SECCIONES_HUMANIZADAS_REVISION.md - Solo secciones humanizadas
3. modelo_negocio_humanizado_final.md - Seccion 5 humanizada
4. marketing_humanizado_final.md - Seccion 10 humanizada
"""
    
    guardar('RESUMEN_MEJORAS_HUMANIZADAS.md', mejoras)
    print("Resumen de mejoras guardado")
    
    print("\nTODOS LOS ARCHIVOS CREADOS:")
    print("1. Plan_Negocio_Treqe_COMPLETO_HUMANIZADO.md")
    print("2. Treqe_SECCIONES_HUMANIZADAS_REVISION.md")
    print("3. RESUMEN_MEJORAS_HUMANIZADAS.md")
    print("\nListo para revisión.")

if __name__ == '__main__':
    main()