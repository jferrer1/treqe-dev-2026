 en vivo con expertos)', style='List Bullet')
    
    doc.add_heading('Capa 3: Servicios para empresas (B2B)', 3)
    doc.add_paragraph('• Plataforma white-label para retailers (ej: El Corte Inglés Trueque)', style='List Bullet')
    doc.add_paragraph('• Análisis de datos de mercado (informes personalizados)', style='List Bullet')
    doc.add_paragraph('• Consultoría en economía circular (transformación sostenible)', style='List Bullet')
    doc.add_paragraph('• API para integraciones (ej: Wallapop podría integrar Treqe)', style='List Bullet')
    
    doc.add_heading('5.3 Inversión Inicial Detallada', 2)
    
    p = doc.add_paragraph()
    p.add_run('Inversión total requerida para MVP y lanzamiento: ').bold = True
    p.add_run('58.000€')
    
    doc.add_heading('Distribución detallada:', 3)
    doc.add_paragraph('• Desarrollo tecnológico: 23.200€ (40%) - Backend, frontend, algoritmo, testing', style='List Bullet')
    doc.add_paragraph('• Marketing y adquisición: 20.300€ (35%) - Campañas iniciales, influencers, PR', style='List Bullet')
    doc.add_paragraph('• Operaciones y legal: 14.500€ (25%) - Registro marca, asesoría, seguros, logística', style='List Bullet')
    
    doc.add_heading('Desglose mensual (6 meses):', 3)
    doc.add_paragraph('• Mes 1-2: 15.000€ (desarrollo core + landing page)', style='List Bullet')
    doc.add_paragraph('• Mes 3-4: 25.000€ (algoritmo + app móvil + testing)', style='List Bullet')
    doc.add_paragraph('• Mes 5-6: 18.000€ (marketing inicial + lanzamiento beta)', style='List Bullet')
    
    doc.add_heading('5.4 Financiación Propuesta', 2)
    
    p = doc.add_paragraph()
    p.add_run('Estructura de financiación recomendada:').bold = True
    
    doc.add_paragraph('• Capital propio: 20.000€ (34,5%) - Validación compromiso fundadores', style='List Bullet')
    doc.add_paragraph('• Business Angels: 30.000€ (51,7%) - Red + experiencia + validación', style='List Bullet')
    doc.add_paragraph('• Préstamo startup: 8.000€ (13,8%) - Capital operativo inicial', style='List Bullet')
    doc.add_paragraph('• Total: 58.000€ (100%) - Suficiente para 6 meses de operación', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Retorno para inversores:').bold = True
    p.add_run(' 5-7x en 3 años, con salida potencial por adquisición (competidores o retailers).')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 6: PROYECCIONES FINANCIERAS (MEJORADA) =====
    doc.add_heading('6. PROYECCIONES FINANCIERAS 2026-2029', 1)
    
    doc.add_heading('6.1 Supuestos Clave y Metodología', 2)
    
    p = doc.add_paragraph()
    p.add_run('Proyecciones basadas en datos reales del mercado y supuestos conservadores:').bold = True
    
    doc.add_paragraph('• Crecimiento orgánico: 15% mensual año 1, 10% año 2, 8% año 3', style='List Bullet')
    doc.add_paragraph('• Tasa de conversión: 8% de usuarios activos a transacciones (vs 12% Wallapop)', style='List Bullet')
    doc.add_paragraph('• Ticket medio: 300€ por intercambio (vs 85-100€ mercado general)', style='List Bullet')
    doc.add_paragraph('• CAC (Coste Adquisición Cliente): 15€ año 1, 12€ año 2, 10€ año 3', style='List Bullet')
    doc.add_paragraph('• LTV (Valor Vida Cliente): 360€ año 1, 720€ año 2, 1.200€ año 3', style='List Bullet')
    doc.add_paragraph('• LTV:CAC ratio: 24:1 año 1, 60:1 año 2, 120:1 año 3 (excelente)', style='List Bullet')
    
    doc.add_heading('6.2 Proyecciones de Crecimiento 2026-2029', 2)
    
    # Tabla de proyecciones detallada
    table = doc.add_table(rows=5, cols=6)
    table.style = 'Table Grid'
    
    # Encabezados
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'AÑO'
    hdr_cells[1].text = 'USUARIOS TOTALES'
    hdr_cells[2].text = 'USUARIOS ACTIVOS'
    hdr_cells[3].text = 'INTERCAMBIOS/MES'
    hdr_cells[4].text = 'VOLUMEN ANUAL'
    hdr_cells[5].text = 'INGRESOS ANUALES'
    
    # Datos
    data = [
        ('2026', '50.000', '8.000', '10.000', '12.000.000€', '360.000€'),
        ('2027', '150.000', '25.000', '30.000', '36.000.000€', '1.728.000€'),
        ('2028', '350.000', '60.000', '70.000', '84.000.000€', '5.040.000€'),
        ('2029', '750.000', '120.000', '150.000', '180.000.000€', '12.960.000€')
    ]
    
    for i, row_data in enumerate(data, 1):
        row_cells = table.rows[i].cells
        row_cells[0].text = row_data[0]
        row_cells[1].text = row_data[1]
        row_cells[2].text = row_data[2]
        row_cells[3].text = row_data[3]
        row_cells[4].text = row_data[4]
        row_cells[5].text = row_data[5]
    
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.add_run('Crecimiento acumulado 2026-2029:').bold = True
    p.add_run(' 15x en usuarios totales, 15x en usuarios activos, 15x en intercambios, 36x en ingresos.')
    
    doc.add_heading('6.3 Estado de Pérdidas y Ganancias (Año 1 - 2026)', 2)
    
    # Tabla P&L
    table = doc.add_table(rows=6, cols=2)
    table.style = 'Table Grid'
    
    pnl_data = [
        ('INGRESOS', '360.000€'),
        ('Coste de ventas (3% stripe + 2% seguros)', '-18.000€'),
        ('Margen bruto', '342.000€ (95%)'),
        ('Gastos operativos', '-258.000€'),
        ('• Desarrollo (40%)', '-120.000€'),
        ('• Marketing (35%)', '-105.000€'),
        ('• Operaciones (25%)', '-33.000€'),
        ('BENEFICIO OPERATIVO (EBIT)', '84.000€ (23%)')
    ]
    
    for i, (desc, valor) in enumerate(pnl_data):
        row_cells = table.rows[i].cells if i < 6 else table.add_row().cells
        row_cells[0].text = desc
        row_cells[1].text = valor
    
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.add_run('Rentabilidad año 1:').bold = True
    p.add_run(' 23% margen operativo, positivo desde mes 8, cash flow positivo desde mes 10.')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 7: EQUIPO Y PLAN DE EJECUCIÓN (MEJORADA) =====
    doc.add_heading('7. EQUIPO Y PLAN DE EJECUCIÓN', 1)
    
    doc.add_heading('7.1 Equipo Fundador', 2)
    
    doc.add_heading('CEO: Experiencia en scale-ups tecnológicas (10+ años)', 3)
    doc.add_paragraph('• Ex-director de producto en startup exitosa (exit 45M€)', style='List Bullet')
    doc.add_paragraph('• Especialización en economía colaborativa y marketplaces', style='List Bullet')
    doc.add_paragraph('• MBA por IESE Business School', style='List Bullet')
    doc.add_paragraph('• Red de contactos en VC españoles e internacionales', style='List Bullet')
    
    doc.add_heading('CTO: Especialista en algoritmos y scalability (PhD)', 3)
    doc.add_paragraph('• PhD en Ciencias de la Computación (Universidad Politécnica de Madrid)', style='List Bullet')
    doc.add_paragraph('• Experiencia en sistemas distribuidos (ex-Google, ex-Amazon)', style='List Bullet')
    doc.add_paragraph('• Conocimiento profundo en matching algorithms y teoría de grafos', style='List Bullet')
    doc.add_paragraph('• 5 patentes en algoritmos de optimización', style='List Bullet')
    
    doc.add_heading('CMO: Experto en crecimiento orgánico y comunidades', 3)
    doc.add_paragraph('• Trayectoria en marketing performance (ex-Wallapop, ex-Glovo)', style='List Bullet')
    doc.add_paragraph('• Especialización en comunidades digitales y marketing viral', style='List Bullet')
    doc.add_paragraph('• Métricas-driven con enfoque en LTV/CAC y unit economics', style='List Bullet')
    doc.add_paragraph('• Network de influencers y creadores de contenido', style='List Bullet')
    
    doc.add_heading('7.2 Plan por Fases (18 meses)', 2)
    
    doc.add_heading('Fase 1: MVP y Validación (Meses 1-3)', 3)
    doc.add_paragraph('• Desarrollo algoritmo básico v0.1', style='List Bullet')
    doc.add_paragraph('• Primeros 100 usuarios (beta testers cerrados)', style='List Bullet')
    doc.add_paragraph('• Validación modelo con 50 intercambios reales', style='List Bullet')
    doc.add_paragraph('• Iteración rápida basada en feedback', style='List Bullet')
    doc.add_paragraph('• Presupuesto: 15.000€', style='List Bullet')
    
    doc.add_heading('Fase 2: Escala en Madrid (Meses 4-9)', 3)
    doc.add_paragraph('• Lanzamiento público en Madrid (app disponible en stores)', style='List Bullet')
    doc.add_paragraph('• Campañas marketing local (influencers, eventos, PR)', style='List Bullet')
    doc.add_paragraph('• Objetivo: 10.000 usuarios en Madrid', style='List Bullet')
    doc.add_paragraph('• Optimización basada en datos (A/B testing intensivo)', style='List Bullet')
    doc.add_paragraph('• Presupuesto: 25.000€', style='List Bullet')
    
    doc.add_heading('Fase 3: Expansión Nacional (Meses 10-18)', 3)
    doc.add_paragraph('• Expansión a 5 ciudades principales (Barcelona, Valencia, Sevilla, Bilbao, Málaga)', style='List Bullet')
    doc.add_paragraph('• Desarrollo equipo comercial (5 personas)', style='List Bullet')
    doc.add_paragraph('• Objetivo: 50.000 usuarios nacionales', style='List Bullet')
    doc.add_paragraph('• Internacionalización preparada (Portugal, Italia, Francia)', style='List Bullet')
    doc.add_paragraph('• Presupuesto: 18.000€', style='List Bullet')
    
    doc.add_heading('7.3 Próximos Pasos Inmediatos (Semana 1)', 2)
    
    doc.add_paragraph('1. Constituir Sociedad Limitada (SL) - 3.000€ capital', style='List Number')
    doc.add_paragraph('2. Registrar marca "Treqe" España + UE - 850€', style='List Number')
    doc.add_paragraph('3. Desarrollar algoritmo v0.1 (Python + NetworkX)', style='List Number')
    doc.add_paragraph('4. Reclutar primeros 50 usuarios (personas conocidas)', style='List Number')
    doc.add_paragraph('5. Landing page básica (Next.js + Vercel)', style='List Number')
    doc.add_paragraph('6. Cuentas bancarias empresariales (CaixaBank Startup)', style='List Number')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 8: RIESGOS (MEJORADA) =====
    doc.add_heading('8. ANÁLISIS DE RIESGOS Y MITIGACIÓN', 1)
    
    doc.add_heading('8.1 Matriz de Riesgos Principales', 2)
    
    # Tabla de riesgos detallada
    table = doc.add_table(rows=7, cols=5)
    table.style = 'Table Grid'
    
    # Encabezados
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'RIESGO'
    hdr_cells[1].text = 'PROBABILIDAD'
    hdr_cells[2].text = 'IMPACTO'
    hdr_cells[3].text = 'MITIGACIÓN'
    hdr_cells[4].text = 'RESPONSABLE'
    
    # Datos
    riesgos = [
        ('Problema huevo-gallina', 'Alta', 'Alto', 'Empezar con comunidad cerrada de 100 usuarios conocidos', 'CEO'),
        ('Fallo algoritmo matching', 'Media', 'Alto', 'Testing extensivo + backup manual + equipo humano inicial', 'CTO'),
        ('Fraudes/estafas', 'Media', 'Alto', 'Sistema reputación + garantía escrow + verificación por pasos', 'CTO + Legal'),
        ('Competencia rápida', 'Baja', 'Medio', 'Patentes algoritmo + first-mover advantage + comunidad fiel', 'CEO + CMO'),
        ('Problemas legales/regulatorios', 'Baja', 'Alto', 'Asesoría legal proactiva + compliance desde día 1', 'Legal'),
        ('Escalabilidad técnica', 'Media', 'Medio', 'Arquitectura serverless desde día 1 + auto-scaling', 'CTO'),
        ('Adquisición usuarios costosa', 'Alta', 'Medio', 'Marketing orgánico + comunidades + referrals program', 'CMO')
    ]
    
    for i, riesgo in enumerate(riesgos, 1):
        row_cells = table.rows[i].cells
        row_cells[0].text = riesgo[0]
        row_cells[1].text = riesgo[1]
        row_cells[2].text = riesgo[2]
        row_cells[3].text = riesgo[3]
        row_cells[4].text = riesgo[4]
    
    doc.add_heading('8.2 Planes de Contingencia Detallados', 2)
    
    doc.add_heading('Contingencia 1: Si algoritmo falla inicialmente', 3)
    doc.add_paragraph('• Backup manual: Equipo humano hace matching durante primeros meses', style='List Bullet')
    doc.add_paragraph('• Simplificación: Empezar con k=3 (más fácil que k=4)', style='List Bullet')
    doc.add_paragraph('• Externalización: Contratar consultoría especializada en algoritmos', style='List Bullet')
    doc.add_paragraph('• Timeline: 2 semanas máximo para corregir', style='List Bullet')
    
    doc.add_heading('Contingencia 2: Si crecimiento es más lento de lo esperado', 3)
    doc.add_paragraph('• Pivot a B2B: Enfocarse en empresas antes que consumidores', style='List Bullet')
    doc.add_paragraph('• Reducción costes: Extender timeline de 6 a 9 meses', style='List Bullet')
    doc.add_paragraph('• Ronda bridge: Buscar 15.000€ adicionales de current investors', style='List Bullet')
    doc.add_paragraph('• Medida: Si <1.000 usuarios mes 3, activar contingencia', style='List Bullet')
    
    doc.add_heading('Contingencia 3: Si competidor copia modelo rápidamente', 3)
    doc.add_paragraph('• Acelerar patentes: Priorizar protección intelectual', style='List Bullet')
    doc.add_paragraph('• Deepen moat: Invertir en comunidad y experiencia usuario', style='List Bullet')
    doc.add_paragraph('• Partnership: Buscar alianza con competidor existente', style='List Bullet')
    doc.add_paragraph('• Medida