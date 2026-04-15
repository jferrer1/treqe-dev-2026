('[ ] 10 personas en lista espera', style='List Bullet')
doc.add_paragraph('[ ] Presupuesto gastado: 4.850€ (de 58.000€)', style='List Bullet')
doc.add_paragraph('[ ] Primeras 5 conversaciones con usuarios', style='List Bullet')

doc.add_heading('Checklist Trimestre 1', level=2)
doc.add_paragraph('[ ] 100 usuarios registrados', style='List Bullet')
doc.add_paragraph('[ ] 20 intercambios completados', style='List Bullet')
doc.add_paragraph('[ ] Sistema web básico funcionando', style='List Bullet')
doc.add_paragraph('[ ] Algoritmo v1.0 automático', style='List Bullet')
doc.add_paragraph('[ ] Soporte básico (email, FAQ)', style='List Bullet')
doc.add_paragraph('[ ] Primeras métricas (CAC, LTV, conversión)', style='List Bullet')
doc.add_paragraph('[ ] Presupuesto gastado: 15.000€ (de 58.000€)', style='List Bullet')
doc.add_paragraph('[ ] Decisión: ¿Continuar o replantear?', style='List Bullet')

doc.add_heading('Checklist Año 1', level=2)
doc.add_paragraph('[ ] 50.000 usuarios totales', style='List Bullet')
doc.add_paragraph('[ ] 8.000 usuarios activos', style='List Bullet')
doc.add_paragraph('[ ] 10.000 intercambios/mes', style='List Bullet')
doc.add_paragraph('[ ] 360.000€ ingresos', style='List Bullet')
doc.add_paragraph('[ ] 84.000€ beneficio', style='List Bullet')
doc.add_paragraph('[ ] Sistema completamente automático', style='List Bullet')
doc.add_paragraph('[ ] App móvil nativa (iOS/Android)', style='List Bullet')
doc.add_paragraph('[ ] Equipo: 5 personas', style='List Bullet')
doc.add_paragraph('[ ] Presupuesto gastado: 58.000€ (completo)', style='List Bullet')
doc.add_paragraph('[ ] Plan año 2 detallado', style='List Bullet')

doc.add_page_break()

# ===== CONCLUSIÓN =====
doc.add_heading('🏁 CONCLUSIÓN', level=1)

p = doc.add_paragraph()
p.add_run('Por qué esto funciona (resumen final):').bold = True

doc.add_paragraph('1. Resuelve un problema real que afecta al 72% de españoles', style='List Number')
doc.add_paragraph('2. Matemáticamente sólido (5% probabilidad → 20-35% con Treqe)', style='List Number')
doc.add_paragraph('3. Modelo económico viable (3% comisión, LTV:CAC 24:1 año 1)', style='List Number')
doc.add_paragraph('4. Escalable tecnológicamente (algoritmo + automatización)', style='List Number')
doc.add_paragraph('5. Protegido legalmente (35.000€ inversión en 3 años)', style='List Number')
doc.add_paragraph('6. Equipo realista (crecimiento progresivo, sin quemar)', style='List Number')
doc.add_paragraph('7. Riesgos identificados y mitigados (8 riesgos + contingencias)', style='List Number')

doc.add_heading('Nuestra ventaja competitiva', level=2)
p = doc.add_paragraph()
p.add_run('No competimos con Wallapop/Vinted en precio. Competimos en ').bold = True
p.add_run('valor.').bold = True

p = doc.add_paragraph()
p.add_run('Ellos: ').bold = True
p.add_run('"Vende por menos, compra por más, pierde tiempo y dinero"')

p = doc.add_paragraph()
p.add_run('Nosotros: ').bold = True
p.add_run('"Consigue lo que quieres, manteniendo el valor, en 72 horas"')

doc.add_heading('Llamada a la acción', level=2)
p = doc.add_paragraph()
p.add_run('Si eres inversor: ').bold = True
p.add_run('58.000€ para capturar un mercado de 15.000 millones €')

p = doc.add_paragraph()
p.add_run('Si eres usuario: ').bold = True
p.add_run('Prueba el primer intercambio gratis (100 primeros)')

p = doc.add_paragraph()
p.add_run('Si eres potencial empleado: ').bold = True
p.add_run('Únete en mes 4-6 cuando escalemos')

p = doc.add_paragraph()
p.add_run('Treqe no es solo una startup. Es una nueva forma de pensar la propiedad.').italic = True

p = doc.add_paragraph()
p.add_run('Porque a veces, lo que tienes ya es lo que quieres. Solo necesitas encontrar a Carlos y Beatriz.').italic = True

# Guardar documento
output_path = os.path.join(os.path.dirname(__file__), 'Plan_Negocio_Treqe_DEFINITIVO_COMPLETO.docx')
doc.save(output_path)

print(f"✅ Documento Word creado exitosamente: {output_path}")
print(f"📄 Tamaño: {os.path.getsize(output_path)} bytes")
print(f"📋 Páginas: Aproximadamente {len(doc.element.xpath('//w:sectPr'))} páginas")
print("\n🎯 Documento incluye:")
print("   • 12 partes completas")
print("   • Todas las skills aplicadas (humanizer, legal, business-model-canvas, marketing-mode)")
print("   • Casos reales con Ana, Carlos, Beatriz")
print("   • Proyecciones financieras año 1-3")
print("   • Cronograma 12 meses paso a paso")
print("   • Aspectos legales completos")
print("   • Riesgos identificados y mitigados")
print("   • Checklists ejecutables")
print("\n📧 ¡Documento listo para usar!")