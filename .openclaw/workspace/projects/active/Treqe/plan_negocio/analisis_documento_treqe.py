#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis del documento Treqe para proponer mejoras.
"""

def analizar_documento_treqe():
    print("="*70)
    print("ANÁLISIS DEL DOCUMENTO: Treqe_Plan_Negocio_ANALISIS.md")
    print("="*70)
    
    with open('Treqe_Plan_Negocio_ANALISIS.md', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    lineas = contenido.split('\n')
    
    # 1. ESTADÍSTICAS BÁSICAS
    print("\n1. ESTADÍSTICAS BÁSICAS:")
    print(f"   • Total líneas: {len(lineas)}")
    print(f"   • Total caracteres: {len(contenido):,}")
    
    # Contar encabezados
    encabezados_n1 = sum(1 for l in lineas if l.startswith('# ') and not l.startswith('##'))
    encabezados_n2 = sum(1 for l in lineas if l.startswith('## ') and not l.startswith('###'))
    encabezados_n3 = sum(1 for l in lineas if l.startswith('### '))
    
    print(f"   • Encabezados nivel 1: {encabezados_n1}")
    print(f"   • Encabezados nivel 2: {encabezados_n2}")
    print(f"   • Encabezados nivel 3: {encabezados_n3}")
    
    # 2. SECCIONES PRINCIPALES
    print("\n2. SECCIONES PRINCIPALES IDENTIFICADAS:")
    
    secciones = [
        ("INTRODUCCIÓN", "1. INTRODUCCIÓN"),
        ("PROBLEMA", "2. EL PROBLEMA"),
        ("SOLUCIÓN", "3. LA SOLUCIÓN"),
        ("VENTAJA COMPETITIVA", "4. POR QUÉ TREQE ES DIFERENTE"),
        ("MODELO DE NEGOCIO", "5. MODELO DE NEGOCIO"),
        ("PROYECCIONES FINANCIERAS", "6. PROYECCIONES FINANCIERAS"),
        ("EQUIPO", "7. EQUIPO"),
        ("RIESGOS", "9. ANÁLISIS DE RIESGOS"),
        ("MARKETING", "10. ESTRATEGIA DE MARKETING"),
        ("LEGAL", "11. ASPECTOS LEGALES"),
        ("PLAN DE SALIDA", "12. PLAN DE SALIDA"),
        ("APÉNDICE", "APÉNDICE")
    ]
    
    for nombre, patron in secciones:
        presente = any(patron in l for l in lineas)
        print(f"   • {nombre}: {'PRESENTE' if presente else 'AUSENTE'}")
    
    # 3. CONTENIDO CLAVE
    print("\n3. CONTENIDO CLAVE VERIFICADO:")
    
    contenido_clave = [
        ("Fórmula scoring", "SCORE_TREQE"),
        ("Ejemplo práctico 4 usuarios", "Ana, Carlos, Beatriz"),
        ("Niveles reputación", "NOVATO"),
        ("Algoritmo k=3", "k=3"),
        ("Ventajas cuantificadas", "75-85%"),
        ("Arquitectura API REST", "API REST"),
        ("Comparación WebSocket", "WebSocket"),
        ("Sistema ofertas estructuradas", "Sistema de Ofertas Estructuradas"),
        ("Sistema garantías combinadas", "Sistema Combinado de Garantías")
    ]
    
    for nombre, texto in contenido_clave:
        presente = texto in contenido
        print(f"   • {nombre}: {'PRESENTE' if presente else 'AUSENTE'}")
    
    # 4. PROBLEMAS DETECTADOS
    print("\n4. PROBLEMAS DETECTADOS:")
    
    # Caracteres de encoding
    caracteres_problematicos = ['�', '�', '�']
    lineas_problematicas = []
    for i, linea in enumerate(lineas):
        for char in caracteres_problematicos:
            if char in linea:
                lineas_problematicas.append(i)
                break
    
    if lineas_problematicas:
        print(f"   • Encoding issues: {len(lineas_problematicas)} líneas con caracteres problemáticos")
    else:
        print("   • Encoding: CORRECTO")
    
    # Secciones muy largas
    print("\n5. ANÁLISIS DE ESTRUCTURA:")
    
    # Encontrar secciones largas
    seccion_actual = ""
    contador_lineas = 0
    secciones_largas = []
    
    for linea in lineas:
        if linea.startswith('# '):
            if contador_lineas > 80 and seccion_actual:  # Más de 80 líneas
                secciones_largas.append((seccion_actual, contador_lineas))
            seccion_actual = linea
            contador_lineas = 0
        elif linea.strip():
            contador_lineas += 1
    
    if secciones_largas:
        print("   • Secciones muy largas (necesitan subdivisión):")
        for seccion, lineas_count in secciones_largas[:3]:  # Mostrar solo 3
            print(f"     - {seccion[:50]}... ({lineas_count} líneas)")
    else:
        print("   • Estructura: BIEN BALANCEADA")
    
    # 6. OPORTUNIDADES DE MEJORA
    print("\n6. OPORTUNIDADES DE MEJORA IDENTIFICADAS:")
    
    oportunidades = []
    
    # Verificar si hay resumen ejecutivo
    if not any("RESUMEN EJECUTIVO" in l.upper() for l in lineas):
        oportunidades.append("Falta resumen ejecutivo al inicio")
    
    # Verificar si hay tabla de contenidos
    if not any("TABLA DE CONTENIDOS" in l.upper() or "ÍNDICE" in l.upper() for l in lineas):
        oportunidades.append("Falta tabla de contenidos navegable")
    
    # Verificar métricas financieras clave
    metricas_financieras = ["ROI", "TIR", "VAN", "payback", "punto de equilibrio"]
    tiene_metricas = any(any(m in l.lower() for m in metricas_financieras) for l in lineas)
    if not tiene_metricas:
        oportunidades.append("Falta análisis financiero detallado (ROI, TIR, VAN)")
    
    # Verificar roadmap temporal
    if not any("ROADMAP" in l.upper() or "CRONOGRAMA" in l.upper() or "TIMELINE" in l.upper() for l in lineas):
        oportunidades.append("Falta roadmap temporal visual")
    
    # Verificar análisis competencia
    if not any("ANÁLISIS COMPETENCIA" in l.upper() or "COMPETIDORES" in l.upper() for l in lineas):
        oportunidades.append("Falta análisis de competencia detallado")
    
    for op in oportunidades:
        print(f"   • {op}")
    
    # 7. PROPUESTAS DE CAMBIO
    print("\n" + "="*70)
    print("PROPUESTAS DE CAMBIO (NO IMPLEMENTADAS - SOLO PROPUESTAS)")
    print("="*70)
    
    propuestas = [
        ("1. RESUMEN EJECUTIVO", "Agregar 1-2 páginas al inicio con: problema, solución, mercado, equipo, financiación, próximos pasos"),
        ("2. TABLA DE CONTENIDOS", "Crear índice navegable con enlaces internos (para versión HTML/PDF)"),
        ("3. ANÁLISIS FINANCIERO", "Profundizar en: ROI por fase, TIR proyecto, VAN 5 años, punto equilibrio detallado"),
        ("4. ROADMAP VISUAL", "Crear timeline con: MVP (meses 1-3), crecimiento (meses 4-12), expansión (año 2)"),
        ("5. ANÁLISIS COMPETENCIA", "Tabla comparativa con: Wallapop, Vinted, Milanuncios, otros marketplaces"),
        ("6. METRICS DASHBOARD", "Sección con KPIs clave: CAC, LTV, churn rate, tasa conversión, NPS"),
        ("7. PLAN DE CONTINGENCIA", "Escenarios: si crecimiento es 50% más lento, si competidor copia, si regulación cambia"),
        ("8. VALIDACIÓN MERCADO", "Evidencia de demanda: encuestas, waitlist, estudios mercado cuantitativos"),
        ("9. EQUIPO DETALLADO", "CVs completos, roles específicos, gaps a cubrir, plan contratación"),
        ("10. PLAN COMUNICACIÓN", "Estrategia PR, relaciones inversores, comunicación crisis, branding")
    ]
    
    for titulo, descripcion in propuestas:
        print(f"\n{titulo}:")
        print(f"   {descripcion}")
    
    print("\n" + "="*70)
    print("PRIORIZACIÓN RECOMENDADA:")
    print("="*70)
    
    prioridades = [
        ("ALTA", "1. Resumen ejecutivo", "Lo primero que ven inversores"),
        ("ALTA", "2. Análisis financiero detallado", "Crítico para decisión inversión"),
        ("MEDIA", "3. Tabla de contenidos navegable", "Mejora experiencia lectura"),
        ("MEDIA", "4. Roadmap visual", "Muestra ejecución concreta"),
        ("MEDIA", "5. Análisis competencia", "Demuestra conocimiento mercado"),
        ("BAJA", "6. Metrics dashboard", "Para versión interna/operaciones")
    ]
    
    for prioridad, item, razon in prioridades:
        print(f"{prioridad}: {item} - {razon}")
    
    print("\n" + "="*70)
    print("NEXT STEPS RECOMENDADOS:")
    print("="*70)
    print("1. Revisar estas propuestas")
    print("2. Decidir cuáles implementar")
    print("3. Definir alcance de cada mejora")
    print("4. Aprobar cambios antes de implementación")
    print("5. Mantener versión Markdown + Word sincronizadas")

if __name__ == "__main__":
    analizar_documento_treqe()