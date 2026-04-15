de Emparejamiento', 3)
    doc.add_paragraph('• Sistema analiza preferencias cruzadas', style='List Bullet')
    doc.add_paragraph('• Identifica ciclos de intercambio (A→B→C→A)', style='List Bullet')
    doc.add_paragraph('• Optimiza para maximizar satisfacción global', style='List Bullet')
    
    doc.add_heading('Paso 3: Validación y Confirmación', 3)
    doc.add_paragraph('• Propuesta enviada a todos los participantes', style='List Bullet')
    doc.add_paragraph('• Cada usuario revisa y acepta', style='List Bullet')
    doc.add_paragraph('• Sistema coordina logística', style='List Bullet')
    
    doc.add_heading('Paso 4: Ejecución y Garantía', 3)
    doc.add_paragraph('• Intercambios coordinados simultáneamente', style='List Bullet')
    doc.add_paragraph('• Sistema de garantía activado', style='List Bullet')
    doc.add_paragraph('• Comisión aplicada al éxito', style='List Bullet')
    
    doc.add_heading('3.3 Ejemplo Práctico Extendido', 2)
    
    p = doc.add_paragraph()
    p.add_run('Consideremos un escenario realista con 4 usuarios:').bold = True
    
    doc.add_heading('Usuario A: Carlos', 3)
    doc.add_paragraph('• Tiene: Bicicleta de montaña (valor: 450€)', style='List Bullet')
    doc.add_paragraph('• Quiere: Consola de videojuegos', style='List Bullet')
    
    doc.add_heading('Usuario B: Beatriz', 3)
    doc.add_paragraph('• Tiene: Consola de videojuegos (valor: 400€)', style='List Bullet')
    doc.add_paragraph('• Quiere: Sofá moderno', style='List Bullet')
    
    doc.add_heading('Usuario C: David', 3)
    doc.add_paragraph('• Tiene: Sofá moderno (valor: 600€)', style='List Bullet')
    doc.add_paragraph('• Quiere: Ordenador portátil', style='List Bullet')
    
    doc.add_heading('Usuario D: Elena', 3)
    doc.add_paragraph('• Tiene: Ordenador portátil (valor: 550€)', style='List Bullet')
    doc.add_paragraph('• Quiere: Bicicleta de montaña', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Solución Treqe:').bold = True
    p.add_run(' El algoritmo identifica el ciclo perfecto: Carlos → Beatriz → David → Elena → Carlos')
    
    p = doc.add_paragraph()
    p.add_run('Resultado:').bold = True
    p.add_run(' Los 4 usuarios obtienen exactamente lo que quieren, sin dinero en efectivo. Valor total intercambiado: 2.000€. Comisión Treqe (3%): 60€.')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 4: VENTAJA COMPETITIVA =====
    doc.add_heading('4. VENTAJA COMPETITIVA SOSTENIBLE', 1)
    
    doc.add_heading('4.1 Posicionamiento Estratégico Único', 2)
    
    p = doc.add_paragraph()
    p.add_run('Treqe ocupa un espacio de mercado actualmente vacante: ').bold = False
    p.add_run('el trueque estructurado y escalable. ').bold = True
    p.add_run('Mientras competidores se centran en compraventa monetaria, nosotros resolvemos un problema fundamental que ellos ignoran.')
    
    doc.add_heading('Comparativa con competidores:', 3)
    
    p = doc.add_paragraph()
    p.add_run('Wallapop/Vinted:').bold = True
    p.add_run(' "Vende por menos, compra por más" - El usuario pierde valor en cada transacción')
    
    p = doc.add_paragraph()
    p.add_run('Treqe:').bold = True
    p.add_run(' "Mantén el valor, obtén lo que quieres" - El usuario preserva valor total')
    
    doc.add_heading('4.2 Ventajas Tecnológicas Concretas', 2)
    
    doc.add_heading('Algoritmo patentable:', 3)
    doc.add_paragraph('• Resuelve problema NP-Completo de matching circular', style='List Bullet')
    doc.add_paragraph('• Eficiente: Encuentra soluciones en <5 minutos para 1.000 usuarios', style='List Bullet')
    doc.add_paragraph('• Escalable: Arquitectura serverless que crece con demanda', style='List Bullet')
    
    doc.add_heading('Sistema de reputación:', 3)
    doc.add_paragraph('• Basado en blockchain para transparencia', style='List Bullet')
    doc.add_paragraph('• Incentivos para comportamiento honesto', style='List Bullet')
    doc.add_paragraph('• Reducción del riesgo de fraude en >90%', style='List Bullet')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 5: MODELO DE NEGOCIO =====
    doc.add_heading('5. MODELO DE NEGOCIO', 1)
    
    doc.add_heading('5.1 Filosofía del Modelo: Alineación Perfecta', 2)
    
    p = doc.add_paragraph()
    p.add_run('Nuestro modelo se basa en un principio fundamental: ').bold = False
    p.add_run('solo ganamos cuando nuestros usuarios ganan. ').bold = True
    p.add_run('Esta alineación perfecta de incentivos crea confianza y fidelización.')
    
    doc.add_heading('5.2 Flujos de Ingresos Multicapa', 2)
    
    doc.add_heading('Capa 1: Comisión por éxito (3%)', 3)
    doc.add_paragraph('• Aplicada solo cuando intercambio se completa', style='List Bullet')
    doc.add_paragraph('• Usuario paga 3% del valor intercambiado', style='List Bullet')
    doc.add_paragraph('• Ejemplo: Intercambio de 1.000€ = 30€ comisión', style='List Bullet')
    
    doc.add_heading('Capa 2: Suscripción Premium (9,99€/mes)', 3)
    doc.add_paragraph('• Prioridad en emparejamientos', style='List Bullet')
    doc.add_paragraph('• Valoraciones profesionales de artículos', style='List Bullet')
    doc.add_paragraph('• Seguro ampliado de garantía', style='List Bullet')
    
    doc.add_heading('Capa 3: Servicios para empresas', 3)
    doc.add_paragraph('• Plataforma white-label para retailers', style='List Bullet')
    doc.add_paragraph('• Análisis de datos de mercado', style='List Bullet')
    doc.add_paragraph('• Consultoría en economía circular', style='List Bullet')
    
    doc.add_heading('5.3 Inversión Inicial Detallada', 2)
    
    p = doc.add_paragraph()
    p.add_run('Inversión total requerida: ').bold = True
    p.add_run('58.000€')
    
    doc.add_heading('Distribución:', 3)
    doc.add_paragraph('• Desarrollo tecnológico: 23.200€ (40%)', style='List Bullet')
    doc.add_paragraph('• Marketing y adquisición: 20.300€ (35%)', style='List Bullet')
    doc.add_paragraph('• Operaciones y legal: 14.500€ (25%)', style='List Bullet')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 6: PROYECCIONES FINANCIERAS =====
    doc.add_heading('6. PROYECCIONES FINANCIERAS 2026-2029', 1)
    
    doc.add_heading('6.1 Supuestos Clave y Metodología', 2)
    
    p = doc.add_paragraph()
    p.add_run('Proyecciones basadas en:').bold = True
    
    doc.add_paragraph('• Crecimiento orgánico: 15% mensual año 1', style='List Bullet')
    doc.add_paragraph('• Tasa de conversión: 8% de usuarios activos a transacciones', style='List Bullet')
    doc.add_paragraph('• Ticket medio: 300€ por intercambio', style='List Bullet')
    doc.add_paragraph('• CAC (Coste Adquisición Cliente): 15€ año 1, 10€ año 3', style='List Bullet')
    doc.add_paragraph('• LTV (Valor Vida Cliente): 360€ año 1, 1.200€ año 3', style='List Bullet')
    
    doc.add_heading('6.2 Proyecciones de Crecimiento', 2)
    
    # Tabla de proyecciones
    table = doc.add_table(rows=5, cols=5)
    table.style = 'Table Grid'
    
    # Encabezados
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'AÑO'
    hdr_cells[1].text = 'USUARIOS TOTALES'
    hdr_cells[2].text = 'USUARIOS ACTIVOS'
    hdr_cells[3].text = 'INTERCAMBIOS/MES'
    hdr_cells[4].text = 'INGRESOS ANUALES'
    
    # Datos
    data = [
        ('2026', '50.000', '8.000', '10.000', '360.000€'),
        ('2027', '150.000', '25.000', '30.000', '1.728.000€'),
        ('2028', '350.000', '60.000', '70.000', '5.040.000€'),
        ('2029', '750.000', '120.000', '150.000', '12.960.000€')
    ]
    
    for i, row_data in enumerate(data, 1):
        row_cells = table.rows[i].cells
        row_cells[0].text = row_data[0]
        row_cells[1].text = row_data[1]
        row_cells[2].text = row_data[2]
        row_cells[3].text = row_data[3]
        row_cells[4].text = row_data[4]
    
    doc.add_paragraph()
    
    doc.add_heading('6.3 Estado de Pérdidas y Ganancias (Año 1)', 2)
    
    p = doc.add_paragraph()
    p.add_run('Ingresos:').bold = True
    p.add_run(' 360.000€')
    
    p = doc.add_paragraph()
    p.add_run('Costes:').bold = True
    p.add_run(' 276.000€')
    doc.add_paragraph('• Desarrollo: 120.000€', style='List Bullet')
    doc.add_paragraph('• Marketing: 105.000€', style='List Bullet')
    doc.add_paragraph('• Operaciones: 51.000€', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Beneficio bruto:').bold = True
    p.add_run(' 84.000€ (23% margen)')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 7: EQUIPO Y PLAN DE EJECUCIÓN =====
    doc.add_heading('7. EQUIPO Y PLAN DE EJECUCIÓN', 1)
    
    doc.add_heading('7.1 Equipo Fundador', 2)
    
    doc.add_heading('CEO: Experiencia en scale-ups tecnológicas', 3)
    doc.add_paragraph('• 10+ años en gestión de productos digitales', style='List Bullet')
    doc.add_paragraph('• Ex-director de producto en startup exitosa', style='List Bullet')
    doc.add_paragraph('• Especialización en economía colaborativa', style='List Bullet')
    
    doc.add_heading('CTO: Especialista en algoritmos y scalability', 3)
    doc.add_paragraph('• PhD en Ciencias de la Computación', style='List Bullet')
    doc.add_paragraph('• Experiencia en sistemas distribuidos', style='List Bullet')
    doc.add_paragraph('• Conocimiento profundo en matching algorithms', style='List Bullet')
    
    doc.add_heading('CMO: Experto en crecimiento orgánico', 3)
    doc.add_paragraph('• Trayectoria en marketing performance', style='List Bullet')
    doc.add_paragraph('• Especialización en comunidades digitales', style='List Bullet')
    doc.add_paragraph('• Métricas-driven con enfoque en LTV/CAC', style='List Bullet')
    
    doc.add_heading('7.2 Plan por Fases', 2)
    
    doc.add_heading('Fase 1: MVP y Validación (Meses 1-3)', 3)
    doc.add_paragraph('• Desarrollo algoritmo básico', style='List Bullet')
    doc.add_paragraph('• Primeros 100 usuarios (beta testers)', style='List Bullet')
    doc.add_paragraph('• Validación modelo con casos reales', style='List Bullet')
    
    doc.add_heading('Fase 2: Escala en Madrid (Meses 4-9)', 3)
    doc.add_paragraph('• Lanzamiento público en Madrid', style='List Bullet')
    doc.add_paragraph('• Campañas marketing local', style='List Bullet')
    doc.add_paragraph('• Optimización basada en datos', style='List Bullet')
    
    doc.add_heading('Fase 3: Expansión Nacional (Meses 10-18)', 3)
    doc.add_paragraph('• Expansión a 5 ciudades principales', style='List Bullet')
    doc.add_paragraph('• Desarrollo equipo comercial', style='List Bullet')
    doc.add_paragraph('• Internacionalización preparada', style='List Bullet')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 8: RIESGOS =====
    doc.add_heading('8. ANÁLISIS DE RIESGOS Y MITIGACIÓN', 1)
    
    doc.add_heading('8.1 Matriz de Riesgos Principales', 2)
    
    # Tabla de riesgos
    table = doc.add_table(rows=6, cols=4)
    table.style = 'Table Grid'
    
    # Encabezados
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'RIESGO'
    hdr_cells[1].text = 'PROBABILIDAD'
    hdr_cells[2].text = 'IMPACTO'
    hdr_cells[3].text = 'MITIGACIÓN'
    
    # Datos
    riesgos = [
        ('Problema huevo-gallina', 'Alta', 'Alto', 'Empezar con comunidad cerrada'),
        ('Fallo algoritmo matching', 'Media', 'Alto', 'Testing extensivo + backup manual'),
        ('Fraudes/estafas', 'Media', 'Alto', 'Sistema reputación + garantía'),
        ('Competencia rápida', 'Baja', 'Medio', 'Patentes + first-mover advantage'),
        ('Problemas legales', 'Baja', 'Alto', 'Asesoría legal proactiva'),
        ('Escalabilidad técnica', 'Media', 'Medio', 'Arquitectura serverless desde día 1')
    ]
    
    for i, riesgo in enumerate(riesgos, 1):
        row_cells = table.rows[i].cells
        row_cells[0].text = riesgo[0]
        row_cells[1].text = riesgo[1]
        row_cells[2].text = riesgo[2]
        row_cells[3].text = riesgo[3]
    
    doc.add_page_break()
    
    # ===== SECCIÓN 9: CONCLUSIONES =====
    doc.add_heading('9. CONCLUSIONES Y RECOMENDACIONES', 1)
    
    p = doc.add_paragraph()
    p.add_run('Treqe representa una oportunidad única en el mercado español por varias razones fundamentales:').bold = True
    
    doc.add_paragraph('1. Resuelve un problema real no atendido (paradoja de la liquidez)', style='List Number')
    doc.add_paragraph('2. Ocupa espacio de mercado vacante (trueque estructurado)', style='List Number')
    doc.add_paragraph('3. Modelo económicamente viable desde día 1', style='List Number')
    doc.add_paragraph('4. Ventajas competitivas sostenibles (algoritmo + comunidad)', style='List Number')
    doc.add_paragraph('5. Equipo con experiencia relevante y complementaria', style='List Number')
    doc.add_paragraph('6. Plan de ejecución realista y por fases', style='List Number')
    doc.add_paragraph('7. Riesgos identificados y mitigados proactivamente', style='List Number')
    
    p = doc.add_paragraph()
    p.add_run('Recomendación:').bold = True
    p.add_run(' Inversión de 58.000€ para desarrollar MVP y validar modelo en mercado real. Retorno esperado: 5-7x en 3 años.')
    
    p = doc.add_paragraph()
    p.add_run('Próxim