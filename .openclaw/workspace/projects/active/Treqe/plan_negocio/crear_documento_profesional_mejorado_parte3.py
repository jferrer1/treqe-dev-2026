os pasos inmediatos:').bold = True
    p.add_run(' Constituir SL, registrar marca, desarrollar algoritmo v0.1, reclutar primeros 50 usuarios.')
    
    # ===== APÉNDICES =====
    doc.add_page_break()
    doc.add_heading('APÉNDICES', 1)
    
    doc.add_heading('Apéndice A: Detalles Técnicos del Algoritmo', 2)
    
    p = doc.add_paragraph()
    p.add_run('El algoritmo de Treqe resuelve el problema de matching circular, que es NP-Completo en su forma general. Nuestra implementación utiliza:').bold = False
    
    doc.add_paragraph('• Heurísticas greedy optimizadas para casos reales', style='List Bullet')
    doc.add_paragraph('• Búsqueda limitada en profundidad (max k=4 usuarios por rueda)', style='List Bullet')
    doc.add_paragraph('• Optimización por simulated annealing para casos complejos', style='List Bullet')
    doc.add_paragraph('• Tiempo de ejecución garantizado <5 minutos para 1.000 usuarios', style='List Bullet')
    
    doc.add_heading('Apéndice B: Plan de Marketing Detallado', 2)
    
    p = doc.add_paragraph()
    p.add_run('Estrategia en 5 fases:').bold = True
    
    doc.add_paragraph('1. Internal (Pre-Lanzamiento): Comunidad cerrada de early adopters', style='List Number')
    doc.add_paragraph('2. Alpha (Beta Privada): 100 usuarios, feedback intensivo', style='List Number')
    doc.add_paragraph('3. Beta (Vista Previa Pública): Madrid, crecimiento orgánico', style='List Number')
    doc.add_paragraph('4. Early Access (Preparación): 5 ciudades, optimización CAC', style='List Number')
    doc.add_paragraph('5. Full Launch (Lanzamiento): España completa, campañas masivas', style='List Number')
    
    doc.add_heading('Apéndice C: Análisis Legal', 2)
    
    p = doc.add_paragraph()
    p.add_run('Estructura recomendada: Sociedad Limitada (SL)').bold = True
    
    doc.add_paragraph('• Capital mínimo: 3.000€', style='List Bullet')
    doc.add_paragraph('• Responsabilidad limitada de socios', style='List Bullet')
    doc.add_paragraph('• Fiscalidad favorable para startups', style='List Bullet')
    doc.add_paragraph('• Protección propiedad intelectual: patente algoritmo + marca registrada', style='List Bullet')
    
    # ===== FIN DEL DOCUMENTO =====
    doc.add_page_break()
    
    # Página final
    final = doc.add_paragraph()
    final.alignment = WD_ALIGN_PARAGRAPH.CENTER
    final.add_run('--- FIN DEL DOCUMENTO ---\n').font.size = Pt(14)
    final.add_run('\n')
    final.add_run('Treqe SL\n').font.size = Pt(12)
    final.add_run('Plataforma de Trueque Inteligente\n').font.size = Pt(12)
    final.add_run(f'Documento generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n').font.size = Pt(10)
    final.add_run('Confidencial - No distribuir\n').font.size = Pt(10)
    
    # Guardar documento
    output_path = os.path.join(os.path.dirname(__file__), 'Plan_Negocio_Treqe_PROFESIONAL_MEJORADO.docx')
    doc.save(output_path)
    
    return output_path

if __name__ == '__main__':
    try:
        print("🚀 Creando documento Word profesional mejorado...")
        print("📋 Aplicando todas las skills necesarias:")
        print("   • humanizer (lenguaje natural pero profesional)")
        print("   • legal (estructura SL, protección IP)")
        print("   • business-model-canvas (modelo multicapa)")
        print("   • marketing-mode (estrategia 5 fases)")
        print("   • frontend-design (experiencia usuario)")
        print("   • algorithm-solver (explicación técnica)")
        
        output_file = crear_documento_profesional()
        file_size = os.path.getsize(output_file)
        
        print(f"\n✅ ¡DOCUMENTO PROFESIONAL MEJORADO CREADO!")
        print(f"📄 Archivo: {output_file}")
        print(f"📏 Tamaño: {file_size:,} bytes (vs 55,164 bytes del anterior)")
        print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("\n🎯 Documento incluye 9 secciones completas + apéndices:")
        print("   1. Introducción (contexto mercado 2025-2026)")
        print("   2. Problema (paradoja de la liquidez)")
        print("   3. Solución (ruedas intercambio inteligente)")
        print("   4. Ventaja competitiva (posicionamiento único)")
        print("   5. Modelo de negocio (flujos multicapa)")
        print("   6. Proyecciones financieras 2026-2029")
        print("   7. Equipo y plan de ejecución")
        print("   8. Análisis de riesgos y mitigación")
        print("   9. Conclusiones y recomendaciones")
        print("   + Apéndices técnicos, marketing, legal")
        print("\n📊 Mejoras respecto al documento anterior:")
        print("   • Más detallado (ejemplos concretos, datos actualizados)")
        print("   • Más profesional (índice, numeración, estructura)")
        print("   • Skills aplicadas correctamente")
        print("   • Lenguaje humano pero profesional")
        print("   • Casos reales (Ana, Carlos, Beatriz, David, Elena)")
        print("   • Tablas y formatos profesionales")
        print("\n📧 ¡Documento listo para presentar a inversores!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()