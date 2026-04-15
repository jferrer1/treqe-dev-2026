let')
doc.add_paragraph('• Presupuesto gastado: 45.000€ (de 58.000€)', style='List Bullet')

doc.add_heading('Mes 10-12: España entera + consolidación', level=2)
doc.add_paragraph('• Mes 10: Estrategia nacional (10.000 usuarios)', style='List Bullet')
doc.add_paragraph('• Mes 11: Automatización total (20.000 usuarios)', style='List Bullet')
doc.add_paragraph('• Mes 12: Consolidación y plan año 2', style='List Bullet')
doc.add_paragraph('• Objetivo final: 50.000 usuarios total', style='List Bullet')
doc.add_paragraph('• Presupuesto gastado: 58.000€ (completo)', style='List Bullet')
doc.add_paragraph('• Ingresos año 1 objetivo: 360.000€', style='List Bullet')
doc.add_paragraph('• Beneficio año 1 objetivo: 84.000€', style='List Bullet')

doc.add_page_break()

# ===== PARTE 7: EQUIPO Y CONTRATACIONES =====
doc.add_heading('👥 PARTE 6: EQUIPO Y CONTRATACIONES', level=1)

doc.add_heading('Fase 1: Fundador solo (Mes 1-3)', level=2)
doc.add_paragraph('• Fundador: Todo (tecnología + negocio + comunidad + marketing)', style='List Bullet')
doc.add_paragraph('• Externo: Abogado (500€/mes) + Contable (300€/mes)', style='List Bullet')
doc.add_paragraph('• Total coste: 800€/mes', style='List Bullet')

doc.add_heading('Fase 2: Primeras contrataciones (Mes 4-6)', level=2)
doc.add_paragraph('• CTO part-time (mes 4): 20h/semana, 1.500€/mes', style='List Bullet')
doc.add_paragraph('• Marketing/Comunidad part-time (mes 5): 10h/semana, 800€/mes', style='List Bullet')
doc.add_paragraph('• Total equipo mes 6: 3.100€/mes', style='List Bullet')

doc.add_heading('Fase 3: Expansión (Mes 7-9)', level=2)
doc.add_paragraph('• 3 personas locales part-time (Barcelona, Valencia, Sevilla)', style='List Bullet')
doc.add_paragraph('• 800€/mes cada una', style='List Bullet')
doc.add_paragraph('• Total equipo mes 9: 5.500€/mes', style='List Bullet')

doc.add_heading('Fase 4: Consolidación (Mes 10-12)', level=2)
doc.add_paragraph('• Evaluar conversiones part-time → full-time', style='List Bullet')
doc.add_paragraph('• Total equipo mes 12: 5.000-7.000€/mes', style='List Bullet')

doc.add_page_break()

# ===== PARTE 8: ASPECTOS LEGALES =====
doc.add_heading('⚖️ PARTE 7: ASPECTOS LEGALES', level=1)

doc.add_heading('Estructura: Sociedad Limitada (SL)', level=2)
doc.add_paragraph('• Capital: 3.000€', style='List Bullet')
doc.add_paragraph('• Ventajas: Responsabilidad limitada, fiscalidad favorable startups', style='List Bullet')
doc.add_paragraph('• Coste constitución: 3.500€ (3.000€ capital + 500€ gestoría)', style='List Bullet')

doc.add_heading('Protección propiedad intelectual', level=2)
doc.add_paragraph('• Algoritmo: Secreto comercial (año 1) → Patente europea (año 2)', style='List Bullet')
doc.add_paragraph('• Marca "Treqe": Registro España + UE (850€)', style='List Bullet')
doc.add_paragraph('• Clases: 35 (intermediación), 9 (software), 42 (tecnología)', style='List Bullet')

doc.add_heading('Presupuesto legal 3 años: 35.000€', level=2)
doc.add_paragraph('• Año 1: 8.000€ (SL, marca, términos básicos)', style='List Bullet')
doc.add_paragraph('• Año 2: 12.000€ (patente, expansión)', style='List Bullet')
doc.add_paragraph('• Año 3: 15.000€ (más protección)', style='List Bullet')

p = doc.add_paragraph()
p.add_run('1,2% de facturación en protección legal nos protege 100% del negocio.').italic = True

doc.add_heading('Contratos clave', level=2)
doc.add_paragraph('• Términos y Condiciones: Claros, lenguaje humano', style='List Bullet')
doc.add_paragraph('• Política Privacidad RGPD: Consentimiento explícito', style='List Bullet')
doc.add_paragraph('• Contrato Escrow: Dinero retenido hasta confirmación', style='List Bullet')

doc.add_page_break()

# ===== PARTE 9: DISEÑO Y EXPERIENCIA =====
doc.add_heading('🎨 PARTE 8: DISEÑO Y EXPERIENCIA', level=1)

doc.add_heading('Dirección estética', level=2)
p = doc.add_paragraph()
p.add_run('"Brutalista digital con toques orgánicos"').italic = True

doc.add_paragraph('• Formas geométricas claras (brutalista)', style='List Bullet')
doc.add_paragraph('• Colores tierra, espacio generoso (orgánico)', style='List Bullet')
doc.add_paragraph('• Tipografía que se lee fácil', style='List Bullet')

doc.add_heading('Paleta de colores', level=2)
doc.add_paragraph('• Primario: #2A2D34 (gris oscuro - seriedad)', style='List Bullet')
doc.add_paragraph('• Secundario: #E8E9EB (gris claro - limpieza)', style='List Bullet')
doc.add_paragraph('• Acento: #C97D60 (terracota - acción)', style='List Bullet')
doc.add_paragraph('• Fondo: #F5F1E6 (crema - calidez)', style='List Bullet')

doc.add_heading('Experiencia usuario (simple y clara)', level=2)
doc.add_paragraph('• Registro: 30 segundos (email + teléfono)', style='List Bullet')
doc.add_paragraph('• Primer intercambio sugerido: 24 horas', style='List Bullet')
doc.add_paragraph('• Soporte: Chat en app, respuesta 2 horas', style='List Bullet')
doc.add_paragraph('• Comunidad: Foro transparente', style='List Bullet')

doc.add_heading('Landing Page (así se ve)', level=2)
p = doc.add_paragraph()
p.add_run('┌─────────────────────────┐').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ TREQE                   │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│                         │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ INTERCAMBIA LO QUE      │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ TIENES POR LO QUE       │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ QUIERES                 │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ En 5 minutos.           │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ Sin regateos.           │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│                         │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ [¿Qué tienes?]          │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ [¿Qué quieres?]         │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('│ [BUSCAR TRUEQUES]       │').font.name = 'Consolas'
p = doc.add_paragraph()
p.add_run('└─────────────────────────┘').font.name = 'Consolas'

doc.add_page_break()

# ===== PARTE 10: RIESGOS Y CONTINGENCIAS =====
doc.add_heading('🚨 PARTE 9: RIESGOS Y CONTINGENCIAS', level=1)

doc.add_heading('Los 8 riesgos principales', level=2)

p = doc.add_paragraph()
p.add_run('1. Problema huevo-gallina').bold = True
doc.add_paragraph('   • Qué: Necesitas usuarios para que funcione, pero necesitas que funcione para tener usuarios', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Alta', style='List Bullet')
doc.add_paragraph('   • Impacto: Alto', style='List Bullet')
doc.add_paragraph('   • Mitigación: Empezar con 50 personas conocidas, intercambios manuales', style='List Bullet')

p = doc.add_paragraph()
p.add_run('2. Algoritmo falla').bold = True
doc.add_paragraph('   • Qué: Sugiere intercambios que no funcionan', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Media', style='List Bullet')
doc.add_paragraph('   • Impacto: Alto', style='List Bullet')
doc.add_paragraph('   • Mitigación: Humanos revisan primeros 100 intercambios', style='List Bullet')

p = doc.add_paragraph()
p.add_run('3. Gastar dinero antes de tiempo').bold = True
doc.add_paragraph('   • Qué: Quemar 58.000€ sin llegar a 8.000 usuarios', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Media', style='List Bullet')
doc.add_paragraph('   • Impacto: Medio', style='List Bullet')
doc.add_paragraph('   • Mitigación: Presupuesto mensual estricto, métricas claras', style='List Bullet')

p = doc.add_paragraph()
p.add_run('4. Competencia copia rápido').bold = True
doc.add_paragraph('   • Qué: Wallapop añade "modo intercambio" en 3 meses', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Baja', style='List Bullet')
doc.add_paragraph('   • Impacto: Alto', style='List Bullet')
doc.add_paragraph('   • Mitigación: Algoritmo complejo, comunidad leal, marca diferente', style='List Bullet')

p = doc.add_paragraph()
p.add_run('5. Problemas legales').bold = True
doc.add_paragraph('   • Qué: Multas por incumplimiento normativo', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Baja', style='List Bullet')
doc.add_paragraph('   • Impacto: Alto', style='List Bullet')
doc.add_paragraph('   • Mitigación: Inversión legal proactiva (35.000€ 3 años)', style='List Bullet')

p = doc.add_paragraph()
p.add_run('6. Fraudes/estafas').bold = True
doc.add_paragraph('   • Qué: Usuarios intentan estafar', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Media', style='List Bullet')
doc.add_paragraph('   • Impacto: Medio', style='List Bullet')
doc.add_paragraph('   • Mitigación: Sistema escrow, verificación usuarios, seguro 1.000€', style='List Bullet')

p = doc.add_paragraph()
p.add_run('7. Problemas logística').bold = True
doc.add_paragraph('   • Qué: Envíos se pierden/dañan', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Media', style='List Bullet')
doc.add_paragraph('   • Impacto: Bajo', style='List Bullet')
doc.add_paragraph('   • Mitigación: Seguro envíos, partners verificados', style='List Bullet')

p = doc.add_paragraph()
p.add_run('8. Escalabilidad técnica').bold = True
doc.add_paragraph('   • Qué: Sistema no escala con crecimiento', style='List Bullet')
doc.add_paragraph('   • Probabilidad: Baja', style='List Bullet')
doc.add_paragraph('   • Impacto: Alto', style='List Bullet')
doc.add_paragraph('   • Mitigación: Arquitectura escalable desde inicio, CTO desde mes 4', style='List Bullet')

doc.add_page_break()

# ===== PARTE 11: ANEXOS Y RECURSOS =====
doc.add_heading('📧 PARTE 10: ANEXOS Y RECURSOS', level=1)

doc.add_heading('Email lanzamiento beta', level=2)
p = doc.add_paragraph()
p.add_run('Asunto: ¡Treqe está vivo! Eres de los primeros').italic = True
doc.add_paragraph()
doc.add_paragraph('Hola [Nombre],')
doc.add_paragraph()
doc.add_paragraph('Te escribo personalmente porque eres una de las primeras 50 personas en probar Treqe.')
doc.add_paragraph()
doc.add_paragraph('¿Recuerdas nuestra conversación sobre [su artículo específico]? Pues Treqe ya puede ayudarte a intercambiarlo.')
doc.add_paragraph()
doc.add_paragraph('Así funciona:')
doc.add_paragraph('1. Entras en treqe.es')
doc.add_paragraph('2. Pones qué tienes y qué te gustaría tener')
doc.add_paragraph('3. En 24 horas te sugerimos intercambios')
doc.add_paragraph()
doc.add_paragraph('Los primeros 100 intercambios son gratis (sin el 3%).')
doc.add_paragraph()
doc.add_paragraph('¿Te animas a probarlo?')
doc.add_paragraph()
doc.add_paragraph('[Tu nombre]')
doc.add_paragraph('Fundador, Treqe')

doc.add_heading('Pitch básico (2 minutos)', level=2)
doc.add_paragraph('Problema: "¿Tienes algo guardado que ya no usas y quieres otra cosa? Intercambiar entre 2 personas tiene solo 5% de probabilidad."')
doc.add_paragraph()
doc.add_paragraph('Solución: "Treqe conecta a 3+ personas para intercambios circulares. Buscamos A→B→C→A, no A→B. Probabilidad sube a 20-35%."')
doc.add_paragraph()
doc.add_paragraph('Modelo: "3% de comisión cuando el intercambio funciona. Solo cobramos cuando tú ganas."')
doc.add_paragraph()
doc.add_paragraph('Tamaño mercado: "15.000 millones € en cosas guardadas en hogares españoles. 65% de la población preferiría intercambiar antes que vender."')
doc.add_paragraph()
doc.add_paragraph('Traction: "Año 1: 8.000 usuarios, 400.000€ ingresos. Año 3: 60.000 usuarios, 2.500.000€ ingresos."')
doc.add_paragraph()
doc.add_paragraph('Equipo: "[Tu nombre], fundador. Experiencia en [tu experiencia]. Apasionado por resolver este problema."')
doc.add_paragraph()
doc.add_paragraph('Petición: "58.000€ para lanzar. 3.000€ para SL, 850€ para marca, resto para tecnología y primeros usuarios."')

doc.add_page_break()

# ===== PARTE 12: CHECKLISTS =====
doc.add_heading('🎯 PARTE 11: CHECKLISTS', level=1)

doc.add_heading('Checklist Semana 1', level=2)
doc.add_paragraph('Legal:', style='List Bullet')
doc.add_paragraph('  [ ] Consultar 3 abogados startups (500€)', style='List Bullet')
doc.add_paragraph('  [ ] Decidir estructura (SL)', style='List Bullet')
doc.add_paragraph('  [ ] Empezar trámites SL (3.500€)', style='List Bullet')
doc.add_paragraph()
doc.add_paragraph('Tecnología:', style='List Bullet')
doc.add_paragraph('  [ ] Registrar dominio treqe.es', style='List Bullet')
doc.add_paragraph('  [ ] Setup hosting básico', style='List Bullet')
doc.add_paragraph('  [ ] Landing page simple', style='List Bullet')
doc.add_paragraph()
doc.add_paragraph('Marketing:', style='List Bullet')
doc.add_paragraph('  [ ] Crear lista 50 personas', style='List Bullet')
doc.add_paragraph('  [ ] Preparar email lanzamiento', style='List Bullet')
doc.add_paragraph('  [ ] Setup Google Analytics', style='List Bullet')

doc.add_heading('Checklist Mes 1', level=2)
doc.add_paragraph('[ ] SL constituida (3.500€)', style='List Bullet')
doc.add_paragraph('[ ] Marca "Treqe" registrada (850€)', style='List Bullet')
doc.add_paragraph('[ ] Dominio treqe.es activo', style='List Bullet')
doc.add_paragraph('[ ] Landing page funcionando', style='List Bullet')
doc.add_paragraph('[ ] Algoritmo v0.1 operativo', style='List Bullet')
doc.add_paragraph