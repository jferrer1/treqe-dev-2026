 Regulación emergente', 3)
    doc.add_paragraph('• Contexto: Nuevas normativas fiscales para ventas entre particulares (2025+)', style='List Bullet')
    doc.add_paragraph('• Tendencia: Profesionalización progresiva del sector', style='List Bullet')
    doc.add_paragraph('• Implicación: Mayor formalidad, mayor confianza del usuario', style='List Bullet')
    
    doc.add_heading('5. Experiencia mobile-first absoluta', 3)
    doc.add_paragraph('• Demografía: 75% del volumen viene de millennials y generación Z', style='List Bullet')
    doc.add_paragraph('• Expectativa: Experiencia perfectamente optimizada para móvil', style='List Bullet')
    doc.add_paragraph('• Imperativo: No tener app móvil excelente = no existir', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Estas tendencias crean un contexto especialmente favorable para Treqe. ').bold = False
    p.add_run('Nuestra plataforma se diseña específicamente para atender estas demandas emergentes del consumidor actual, no las necesidades del consumidor de hace una década.').bold = True
    
    # ===== RESUMEN EJECUTIVO DE ESTA SECCIÓN =====
    doc.add_page_break()
    doc.add_heading('📋 RESUMEN EJECUTIVO DE ESTA SECCIÓN', 1)
    
    p = doc.add_paragraph()
    p.add_run('Esta sección establece el contexto fundamental para entender por qué Treqe tiene sentido AHORA:').bold = True
    
    doc.add_heading('🎯 PUNTOS CLAVE:', 2)
    
    doc.add_heading('1. El mercado ha cambiado radicalmente', 3)
    doc.add_paragraph('• De "opción económica en crisis" a "movimiento cultural con valores"', style='List Bullet')
    doc.add_paragraph('• Usuarios más exigentes: buscan calidad + autenticidad + valores', style='List Bullet')
    doc.add_paragraph('• Crecimiento sostenido: +42% desde 2020, 8.200M€ en 2026', style='List Bullet')
    
    doc.add_heading('2. La competencia deja un espacio vacante', 3)
    doc.add_paragraph('• Wallapop/Vinted: Compraventa monetaria (pierdes valor)', style='List Bullet')
    doc.add_paragraph('• Facebook Marketplace: Gratis pero inseguro', style='List Bullet')
    doc.add_paragraph('• Milanuncios: Tradicional y desactualizado', style='List Bullet')
    doc.add_paragraph('• Espacio vacante: Trueque estructurado y escalable', style='List Bullet')
    
    doc.add_heading('3. Las tendencias juegan a favor', 3)
    doc.add_paragraph('• Premiumización: La segunda mano ya no es "lo barato"', style='List Bullet')
    doc.add_paragraph('• Sostenibilidad: Valores ecológicos guían decisiones', style='List Bullet')
    doc.add_paragraph('• Mobile-first: Experiencia móvil perfecta es obligatoria', style='List Bullet')
    doc.add_paragraph('• Comunidades locales: Confianza geográfica > escala global', style='List Bullet')
    
    doc.add_heading('4. La oportunidad es cuantificable', 3)
    doc.add_paragraph('• Mercado total: 8.200M€ (2026)', style='List Bullet')
    doc.add_paragraph('• Segmento trueque potencial: 1.230M€ (15%)', style='List Bullet')
    doc.add_paragraph('• Usuarios insatisfechos: 17M (60% de usuarios activos)', style='List Bullet')
    doc.add_paragraph('• Valor medio disponible: 1.200€ por usuario', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Esta introducción establece el "por qué ahora" de Treqe. ').bold = False
    p.add_run('No estamos resolviendo un problema pequeño o marginal; estamos abordando una oportunidad masiva en un mercado en transformación, con competidores que han dejado un espacio claro sin cubrir.').bold = True
    
    # ===== INFORMACIÓN DE VERSIÓN =====
    doc.add_page_break()
    info_final = doc.add_paragraph()
    info_final.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info_final.add_run('--- FIN DEL DOCUMENTO 01 ---\n').font.size = Pt(14)
    info_final.add_run('\n')
    info_final.add_run('DOCUMENTO: 01_INTRODUCCION.docx\n').font.size = Pt(12)
    info_final.add_run('PARTE DE: Plan de Negocio Treqe - Estructura Segregada\n').font.size = Pt(12)
    info_final.add_run(f'GENERADO: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n').font.size = Pt(10)
    info_final.add_run('BASADO EN: Plan_Negocio_Treqe_100%_PROFESIONAL_FINAL.docx (25 febrero 9:29)\n').font.size = Pt(10)
    info_final.add_run('SKILLS APLICADAS: humanizer (lenguaje natural), marketing-mode (datos persuasivos)\n').font.size = Pt(10)
    info_final.add_run('ESTADO: Para revisión - Versión 1.0\n').font.size = Pt(10)
    
    # Guardar documento
    output_path = os.path.join(os.path.dirname(__file__), '01_INTRODUCCION.docx')
    doc.save(output_path)
    
    return output_path

if __name__ == '__main__':
    try:
        print("🚀 CREANDO 01_INTRODUCCION.DOCX")
        print("🎯 Referencia exacta: Plan_Negocio_Treqe_100%_PROFESIONAL_FINAL.docx (25 febrero 9:29)")
        print("🔧 Skills aplicadas: humanizer + marketing-mode")
        print("📊 Objetivo: Mantener estructura original + mejorar lenguaje + hacer datos más persuasivos")
        
        output_file = crear_introduccion()
        file_size = os.path.getsize(output_file)
        
        print(f"\n✅ ¡01_INTRODUCCION.DOCX CREADO!")
        print(f"📄 Archivo: {output_file}")
        print(f"📏 Tamaño: {file_size:,} bytes")
        print(f"📅 Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        print("\n🎯 CONTENIDO (4 secciones + resumen):")
        print("   1.1 La Transformación de un Sector Tradicional (humanizer aplicado)")
        print("   1.2 Datos Cuantitativos Actualizados 2025-2026 (marketing-mode aplicado)")
        print("   1.3 El Panorama Competitivo Actual (análisis competencia)")
        print("   1.4 Tendencias Emergentes que Definen el Futuro (5 tendencias clave)")
        print("   + Resumen ejecutivo de la sección")
        
        print("\n🔧 MEJORAS APLICADAS:")
        print("   • humanizer: Lenguaje más natural (\"Si miramos atrás\" vs \"Si echamos la vista atrás\")")
        print("   • humanizer: Frases más conversacionales pero profesionales")
        print("   • marketing-mode: Datos presentados de manera más persuasiva")
        print("   • marketing-mode: Énfasis en oportunidades (¡casi la mitad más en solo 6 años!)")
        print("   • Estructura: Índice interno + resumen ejecutivo al final")
        print("   • Formato: Portada específica para este documento individual")
        
        print("\n📋 PRÓXIMO PASO:")
        print("   Revisar este documento y dar feedback antes de continuar con 02_PROBLEMA_PARADOJA_LIQUIDEZ.docx")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()