 1.200€', style='List Bullet')
    doc.add_paragraph('• Volumen total estimado: ~10.000 millones de euros en valor no realizado', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('La paradoja es clara: ').bold = True
    p.add_run('valor existe, necesidad existe, pero falta mecanismo eficiente para convertir uno en otro.')
    
    doc.add_heading('2.2 Las Opciones No Óptimas Disponibles', 2)
    
    p = doc.add_paragraph()
    p.add_run('Frente a esta situación, los usuarios enfrentan un "trilema" con tres opciones insatisfactorias:').bold = False
    
    doc.add_heading('Opción A: Mantener objetos innecesarios (58% elige esto)', 3)
    doc.add_paragraph('• Ocupación espacio valioso: En ciudades caras, cada m² tiene coste de oportunidad alto', style='List Bullet')
    doc.add_paragraph('• Depreciación continua: Objetos pierden valor con el tiempo (especialmente tecnología/moda)', style='List Bullet')
    doc.add_paragraph('• Coste psicológico: Insatisfacción constante por convivir con objetos no deseados', style='List Bullet')
    doc.add_paragraph('• Inercia acumulativa: Cuanto más tiempo pasa, más difícil cambiar', style='List Bullet')
    
    doc.add_heading('Opción B: Vender por debajo del valor real', 3)
    doc.add_paragraph('• Realidad mercado: Para vender rápido, precio debe ser 30-50% inferior al valor real', style='List Bullet')
    doc.add_paragraph('• Pérdida económica significativa: Ejemplo: vender bicicleta de 450€ por 300€ = pérdida 150€', style='List Bullet')
    doc.add_paragraph('• Frustración: Saber que se "regala" algo que costó esfuerzo adquirir', style='List Bullet')
    doc.add_paragraph('• Desmotivación: Muchos abandonan después de intentos fallidos', style='List Bullet')
    
    doc.add_heading('Opción C: Trueque directo (coincidencia perfecta)', 3)
    doc.add_paragraph('• Probabilidad matemática: ~5% de encontrar coincidencia perfecta 1:1', style='List Bullet')
    doc.add_paragraph('• Limitación fundamental: Requiere que A quiera exactamente lo que B tiene, y viceversa', style='List Bullet')
    doc.add_paragraph('• Ineficiencia extrema: Miles de intentos para un solo éxito', style='List Bullet')
    doc.add_paragraph('• Frustración garantizada: La mayoría abandona después de semanas sin resultados', style='List Bullet')
    
    doc.add_heading('2.3 La Limitación Matemática Fundamental', 2)
    
    p = doc.add_paragraph()
    p.add_run('El problema del trueque tradicional es matemático: ').bold = False
    p.add_run('la probabilidad de coincidencia perfecta entre dos personas es extremadamente baja. ').bold = True
    p.add_run('En un mercado con 1.000 usuarios y 10.000 artículos, la probabilidad de que A quiera exactamente lo que B tiene, y B quiera exactamente lo que A tiene, es inferior al 0,1%.')
    
    p = doc.add_paragraph()
    p.add_run('Esta limitación matemática explica por qué el trueque nunca ha escalado: ').bold = False
    p.add_run('no es un problema de voluntad, sino de probabilidades. ').bold = True
    p.add_run('Sin un mecanismo que supere esta restricción, el trueque seguirá siendo una curiosidad marginal.')
    
    doc.add_heading('2.4 La Oportunidad Cuantificada', 2)
    
    p = doc.add_paragraph()
    p.add_run('La oportunidad es clara y cuantificable: ').bold = False
    p.add_run('10.000 millones de euros en valor atrapado, 28 millones de usuarios potenciales, y un mercado de 8.200 millones de euros que crece al 42% desde 2020.').bold = True
    
    doc.add_paragraph('• Mercado total disponible: 8.200M€ (2026)', style='List Bullet')
    doc.add_paragraph('• Segmento trueque potencial: 1.230M€ (15% del total)', style='List Bullet')
    doc.add_paragraph('• Usuarios insatisfechos con opciones actuales: 17M (60% de usuarios activos)', style='List Bullet')
    doc.add_paragraph('• Valor medio por usuario disponible: 1.200€', style='List Bullet')
    doc.add_paragraph('• Comisión potencial (3%): 36,9M€ anuales en segmento trueque', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Esta oportunidad no es teórica: ').bold = True
    p.add_run('es cuantificable, medible, y alcanzable con la solución tecnológica adecuada.')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 3: LA SOLUCIÓN (MEJORADA) =====
    doc.add_heading('3. LA SOLUCIÓN TREQE: RUEDAS DE INTERCAMBIO INTELIGENTE', 1)
    
    doc.add_heading('3.1 Un Concepto que Supera Limitaciones Históricas', 2)
    
    p = doc.add_paragraph()
    p.add_run('Treqe introduce un concepto revolucionario que resuelve la paradoja de la liquidez: ').bold = False
    p.add_run('las ruedas de intercambio inteligente. ').bold = True
    p.add_run('Este sistema permite a múltiples usuarios intercambiar bienes simultáneamente, creando un mecanismo de trueque escalable y eficiente.')
    
    p = doc.add_paragraph()
    p.add_run('A diferencia del trueque tradicional (que requiere coincidencia perfecta entre dos personas), Treqe utiliza algoritmos avanzados para identificar cadenas de intercambio entre tres o más usuarios. ').bold = False
    p.add_run('Esta innovación matemática aumenta exponencialmente las probabilidades de éxito.')
    
    doc.add_heading('3.2 El Mecanismo Operativo Paso a Paso', 2)
    
    doc.add_heading('Paso 1: Registro y Catálogo (30 segundos)', 3)
    doc.add_paragraph('• Usuario fotografía artículo con móvil', style='List Bullet')
    doc.add_paragraph('• Sistema valora automáticamente (IA + datos mercado)', style='List Bullet')
    doc.add_paragraph('• Usuario indica preferencias (qué quiere recibir)', style='List Bullet')
    doc.add_paragraph('• Perfil creado en menos de 1 minuto', style='List Bullet')
    
    doc.add_heading('Paso 2: Algoritmo de Emparejamiento (cada 5 minutos)', 3)
    doc.add_paragraph('• Sistema analiza preferencias cruzadas de todos los usuarios', style='List Bullet')
    doc.add_paragraph('• Identifica ciclos de intercambio (A→B→C→A)', style='List Bullet')
    doc.add_paragraph('• Optimiza para maximizar satisfacción global', style='List Bullet')
    doc.add_paragraph('• Tiempo máximo: 5 minutos para 1.000 usuarios', style='List Bullet')
    
    doc.add_heading('Paso 3: Validación y Confirmación (24 horas)', 3)
    doc.add_paragraph('• Propuesta enviada a todos los participantes', style='List Bullet')
    doc.add_paragraph('• Cada usuario revisa detalles y acepta', style='List Bullet')
    doc.add_paragraph('• Sistema coordina logística automáticamente', style='List Bullet')
    doc.add_paragraph('• Ventana de confirmación: 24 horas máximo', style='List Bullet')
    
    doc.add_heading('Paso 4: Ejecución y Garantía (3-5 días)', 3)
    doc.add_paragraph('• Intercambios coordinados simultáneamente', style='List Bullet')
    doc.add_paragraph('• Sistema de garantía activado (escrow + seguro)', style='List Bullet')
    doc.add_paragraph('• Comisión aplicada solo al éxito (3%)', style='List Bullet')
    doc.add_paragraph('• Reputación actualizada para todos los participantes', style='List Bullet')
    
    doc.add_heading('3.3 Ejemplo Práctico Extendido', 2)
    
    p = doc.add_paragraph()
    p.add_run('Consideremos un escenario realista con 4 usuarios en Madrid:').bold = True
    
    doc.add_heading('Usuario A: Carlos (28 años, diseñador gráfico)', 3)
    doc.add_paragraph('• Tiene: Bicicleta de montaña Trek (valor: 450€, comprada 2023)', style='List Bullet')
    doc.add_paragraph('• Quiere: Consola PlayStation 5 (para jugar con amigos)', style='List Bullet')
    doc.add_paragraph('• Ubicación: Chamberí, Madrid', style='List Bullet')
    
    doc.add_heading('Usuario B: Beatriz (31 años, profesora universitaria)', 3)
    doc.add_paragraph('• Tiene: Consola PlayStation 5 (valor: 400€, usada 6 meses)', style='List Bullet')
    doc.add_paragraph('• Quiere: Sofá moderno de 3 plazas (para nuevo piso)', style='List Bullet')
    doc.add_paragraph('• Ubicación: Salamanca, Madrid', style='List Bullet')
    
    doc.add_heading('Usuario C: David (35 años, consultor IT)', 3)
    doc.add_paragraph('• Tiene: Sofá moderno de 3 plazas (valor: 600€, comprado 2024)', style='List Bullet')
    doc.add_paragraph('• Quiere: Ordenador portátil MacBook Air (para teletrabajo)', style='List Bullet')
    doc.add_paragraph('• Ubicación: Retiro, Madrid', style='List Bullet')
    
    doc.add_heading('Usuario D: Elena (29 años, periodista freelance)', 3)
    doc.add_paragraph('• Tiene: Ordenador portátil MacBook Air (valor: 550€, modelo 2022)', style='List Bullet')
    doc.add_paragraph('• Quiere: Bicicleta de montaña (para hacer deporte)', style='List Bullet')
    doc.add_paragraph('• Ubicación: Chamberí, Madrid', style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Solución Treqe:').bold = True
    p.add_run(' El algoritmo identifica el ciclo perfecto en menos de 2 minutos: Carlos → Beatriz → David → Elena → Carlos')
    
    p = doc.add_paragraph()
    p.add_run('Resultado:').bold = True
    p.add_run(' Los 4 usuarios obtienen exactamente lo que quieren, sin dinero en efectivo. Valor total intercambiado: 2.000€. Comisión Treqe (3%): 60€. Tiempo total desde registro hasta intercambio: 72 horas.')
    
    p = doc.add_paragraph()
    p.add_run('Beneficios adicionales:').bold = True
    p.add_run(' Todos mantienen el valor de sus artículos, evitan pérdidas por venta rápida, y resuelven necesidades reales sin gastar dinero.')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 4: VENTAJA COMPETITIVA (MEJORADA) =====
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
    p.add_run('Facebook Marketplace:').bold = True
    p.add_run(' "Gratis pero inseguro" - Experiencia básica, riesgos altos, sin garantías')
    
    p = doc.add_paragraph()
    p.add_run('Milanuncios:').bold = True
    p.add_run(' "Tradicional y desactualizado" - Interfaz anticuada, usuarios menos digitalizados')
    
    p = doc.add_paragraph()
    p.add_run('Treqe:').bold = True
    p.add_run(' "Mantén el valor, obtén lo que quieres" - El usuario preserva valor total, con seguridad y garantía')
    
    doc.add_heading('4.2 Ventajas Tecnológicas Concretas', 2)
    
    doc.add_heading('Algoritmo patentable (skill: algorithm-solver):', 3)
    doc.add_paragraph('• Resuelve problema NP-Completo de matching circular', style='List Bullet')
    doc.add_paragraph('• Eficiente: Encuentra soluciones en <5 minutos para 1.000 usuarios', style='List Bullet')
    doc.add_paragraph('• Escalable: Arquitectura serverless que crece con demanda', style='List Bullet')
    doc.add_paragraph('• Optimizado: Heurísticas greedy + simulated annealing para casos complejos', style='List Bullet')
    
    doc.add_heading('Sistema de reputación blockchain (skill: legal):', 3)
    doc.add_paragraph('• Transparencia total: Todas las transacciones verificables', style='List Bullet')
    doc.add_paragraph('• Incentivos para comportamiento honesto', style='List Bullet')
    doc.add_paragraph('• Reducción del riesgo de fraude en >90%', style='List Bullet')
    doc.add_paragraph('• Historial inmutable: Reputación que viaja con el usuario', style='List Bullet')
    
    doc.add_heading('Experiencia usuario mobile-first (skill: frontend-design):', 3)
    doc.add_paragraph('• Diseño "Brutalista digital con toques orgánicos"', style='List Bullet')
    doc.add_paragraph('• Paleta colores: #2A2D34 (gris oscuro), #C97D60 (terracota), #F5F1E6 (crema)', style='List Bullet')
    doc.add_paragraph('• Registro en 30 segundos: Foto + preferencias = perfil completo', style='List Bullet')
    doc.add_paragraph('• PWA instalable: Funciona como app nativa sin tiendas', style='List Bullet')
    
    doc.add_page_break()
    
    # ===== SECCIÓN 5: MODELO DE NEGOCIO (MEJORADA) =====
    doc.add_heading('5. MODELO DE NEGOCIO', 1)
    
    doc.add_heading('5.1 Filosofía del Modelo: Alineación Perfecta', 2)
    
    p = doc.add_paragraph()
    p.add_run('Nuestro modelo se basa en un principio fundamental: ').bold = False
    p.add_run('solo ganamos cuando nuestros usuarios ganan. ').bold = True
    p.add_run('Esta alineación perfecta de incentivos crea confianza y fidelización.')
    
    p = doc.add_paragraph()
    p.add_run('A diferencia de competidores que cobran por listar o por intentos fallidos, Treqe cobra únicamente cuando el intercambio se completa satisfactoriamente. ').bold = False
    p.add_run('Nuestro éxito está intrínsecamente ligado al éxito de nuestros usuarios.').bold = True
    
    doc.add_heading('5.2 Flujos de Ingresos Multicapa (skill: business-model-canvas)', 2)
    
    doc.add_heading('Capa 1: Comisión por éxito (3%)', 3)
    doc.add_paragraph('• Aplicada solo cuando intercambio se completa', style='List Bullet')
    doc.add_paragraph('• Usuario paga 3% del valor intercambiado', style='List Bullet')
    doc.add_paragraph('• Ejemplo: Intercambio de 1.000€ = 30€ comisión', style='List Bullet')
    doc.add_paragraph('• Justificación: Valor creado = valor capturado', style='List Bullet')
    
    doc.add_heading('Capa 2: Suscripción Premium (9,99€/mes)', 3)
    doc.add_paragraph('• Prioridad en emparejamientos (matchmaking 2x más rápido)', style='List Bullet')
    doc.add_paragraph('• Valoraciones profesionales de artículos (certificados de autenticidad)', style='List Bullet')
    doc.add_paragraph('• Seguro ampliado de garantía (hasta 2.000€ de cobertura)', style='List Bullet')
    doc.add_paragraph('• Soporte premium 24/7 (chat