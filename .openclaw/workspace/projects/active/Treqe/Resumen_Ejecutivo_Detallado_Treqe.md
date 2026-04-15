# RESUMEN EJECUTIVO DETALLADO - TREQE
## Plataforma de Trueque Inteligente

**Fecha:** 24 de febrero de 2026  
**Versión:** 1.0 - Documento Profesional  
**Estado:** CONFIDENCIAL

---

## 1. INTRODUCCIÓN Y OPORTUNIDAD ESTRATÉGICA

### Contexto del Mercado (2025-2026)

El mercado de segunda mano en España ha experimentado una transformación estructural sin precedentes en la última década. De representar un sector marginal tradicionalmente asociado a periodos de crisis económica, ha evolucionado hacia un modelo de consumo consciente, sostenible y económicamente inteligente que atrae a todos los segmentos demográficos.

**Datos clave del mercado español (fuentes: informes sectoriales 2025-2026):**

- **Volumen total estimado 2026:** 8.200 millones de euros (+42% desde 2020)
- **Usuarios activos:** 28 millones de españoles (47% de la población)
- **Gasto medio anual por usuario:** 1.850€ (+142% vs 2016)
- **Penetración móvil:** 94% utiliza aplicaciones móviles para transacciones
- **Segmento de lujo:** Crecimiento del 125% entre 2023-2025

**Principales actores competitivos:**
- **Wallapop:** Líder indiscutible con aproximadamente 15 millones de usuarios en España
- **Vinted:** Especializada en moda, con 4,5 millones de usuarios activos
- **Facebook Marketplace:** Potencial de 20 millones de usuarios por integración con red social
- **Milanuncios:** Plataforma tradicional manteniendo 10% de cuota de mercado

### Tendencias Identificadas

1. **Mobile-first absoluto:** 9 de cada 10 transacciones se inician desde dispositivos móviles
2. **Premiumización creciente:** Demanda acelerada de artículos de segunda mano de alta calidad
3. **Sostenibilidad como driver:** 68% de usuarios menciona motivación ecológica como factor clave
4. **Importancia de comunidad:** Redes de confianza local son críticas para transacciones exitosas
5. **Regulación emergente:** Nuevas normativas fiscales para ventas entre particulares (2025+)

---

## 2. PROBLEMA IDENTIFICADO Y OPORTUNIDAD NO CUBIERTA

### Problema Central: Restricción de Liquidez

A pesar del crecimiento exponencial del mercado, existe una limitación fundamental no resuelta por las plataformas actuales: **millones de usuarios desean renovar sus posesiones pero carecen del capital necesario para adquirir nuevos artículos**.

**Situación actual del usuario típico:**
1. **Tiene artículos** que ya no necesita/usa pero que conservan valor
2. **Desea nuevos artículos** que satisfagan necesidades actuales
3. **Carece de liquidez** para comprar directamente
4. **Enfrenta dilema:**
   - Mantener objetos innecesarios (ocupan espacio, deprecian valor)
   - Vender por debajo de valor real (pérdida económica)
   - Postergar renovación (insatisfacción continua)

### Limitación Técnica: Doble Coincidencia de Deseos

El trueque tradicional requiere que dos personas quieran exactamente lo que la otra ofrece, situación que estadísticamente ocurre en menos del 5% de los intentos. Esta limitación matemática ha impedido la escalabilidad del trueque como modelo comercial viable.

### Oportunidad Cuantificada

- **Mercado potencial:** Usuarios que preferirían intercambiar antes que vender: ~8 millones en España
- **Volumen económico:** Valor estimado de artículos "atrapados" en hogares españoles: 15.000 millones de euros
- **Frecuencia deseada:** Usuarios querrían renovar posesiones cada 2-3 años vs cada 5-7 años actualmente
- **Brecha de satisfacción:** 73% de usuarios de plataformas de segunda mano expresan frustración por no poder intercambiar directamente

---

## 3. SOLUCIÓN INNOVADORA: SISTEMA DE RUEDAS DE INTERCAMBIO INTELIGENTE

### Concepto Fundamental

Treqe introduce el concepto de **"ruedas de intercambio"** que permiten la participación de tres o más usuarios en cadenas circulares de valor, resolviendo matemáticamente el problema de la doble coincidencia de deseos.

### Mecanismo Operativo Detallado

**Paso 1: Registro de Preferencias**
- Usuarios indican: "Tengo" (artículos disponibles) + "Quiero" (artículos deseados)
- Especifican valor estimado y condiciones
- Suben fotos y descripciones detalladas

**Paso 2: Algoritmo de Matching (Teoría de Grafos)**
- Sistema construye grafo dirigido: usuarios → artículos deseados
- Busca ciclos cerrados de 3-5 nodos usando DFS optimizado
- Timeout: 500ms por búsqueda para escalabilidad

**Paso 3: Optimización Económica (Programación Lineal)**
- Calcula compensaciones monetarias óptimas usando algoritmo PuLP
- Minimiza transferencias totales
- Maximiza satisfacción global
- Considera preferencias individuales (ubicación, estado artículo, etc.)

**Paso 4: Negociación Facilitada**
- Chat grupal en tiempo real con WebSockets
- Sistema sugiere términos basados en optimización
- Usuarios pueden ajustar condiciones
- Acuerdo requiere confirmación de todos participantes

**Paso 5: Ejecución Segura**
- Pagos procesados vía Stripe Connect (fondos en escrow)
- Logística integrada con APIs Correos/SEUR
- Sistema de reputación y garantías
- Soporte disputas automatizado

### Ejemplo Práctico Detallado

**Situación Inicial:**
- **Ana:** Tiene bicicleta de montaña (valor 450€), necesita sofá de diseño (valor 600€)
- **Carlos:** Tiene sofá de diseño (valor 600€), necesita ordenador portátil gaming (valor 800€)
- **Beatriz:** Tiene ordenador portátil gaming (valor 800€), necesita bicicleta de montaña (valor 450€)

**Problema Tradicional:** Ningún intercambio directo 1:1 es posible

**Solución Treqe:**
1. **Intercambios Físicos:**
   - Ana envía bicicleta a Beatriz
   - Carlos envía sofá a Ana
   - Beatriz envía ordenador a Carlos

2. **Compensaciones Monetarias (calculadas automáticamente):**
   - Ana paga 150€ a Carlos (diferencia: 600€ - 450€)
   - Carlos paga 200€ a Beatriz (diferencia: 800€ - 600€)
   - Beatriz recibe 350€ neto (150€ + 200€)

3. **Resultados Finales:**
   - **Ana:** Recibe sofá valor 600€ por 150€ → **Ahorro: 450€ (75%)**
   - **Carlos:** Recibe ordenador valor 800€ por 200€ → **Ahorro: 600€ (75%)**
   - **Beatriz:** Recibe bicicleta valor 450€ + 350€ neto → **Valor total: 800€**

**Innovación Diferencial:** Sistema híbrido único que combina trueque físico con compensación económica optimizada, resolviendo simultáneamente problemas de liquidez y matching.

---

## 4. VENTAJA COMPETITIVA SOSTENIBLE

### Posicionamiento Único: Primer Mover en Trueque Estructurado

Treqe ocupa un nicho inexplorado por los principales actores del mercado, quienes se centran exclusivamente en compraventa monetaria.

### Ventajas Tecnológicas

**1. Algoritmos Propietarios:**
- Matching basado en teoría de grafos (NetworkX library)
- Optimización lineal para compensaciones (PuLP solver)
- Sistema de reputación con machine learning
- Detección de fraudes con análisis de patrones

**2. Arquitectura Moderna y Escalable:**
- **Frontend:** Next.js 14 + React 19 + TypeScript + PWA (instalable como app nativa)
- **Backend:** Node.js + Express + WebSockets (negociación tiempo real)
- **Matching Service:** Python microservicio con Redis cache
- **Base de datos:** PostgreSQL (ACID compliance) + TimescaleDB para analytics
- **Infraestructura:** Serverless (Vercel + Railway + Cloudinary)
- **APIs integradas:** Stripe Connect, Correos/SEUR, Google Maps, SendGrid

**3. Experiencia de Usuario Superior:**
- Onboarding guiado en 3 minutos
- Interfaz mobile-first optimizada
- Notificaciones push inteligentes
- Soporte multilingüe (ES, EN, CAT)

### Ventajas Económicas

**1. Modelo de Comisiones Disruptivo:**
- **Treqe:** 1% sobre valor artículo adquirido
- **Wallapop:** 5% + 0,90€ fijo por venta
- **Vinted:** 5% + 0,70€ + 3% protección comprador
- **Ventaja competitiva:** 80-90% más barato que competencia

**2. Transparencia Radical:**
- Comisión única y predecible
- Sin costes ocultos
- Pago solo al recibir valor tangible
- Desglose detallado de compensaciones

**3. Alineación Perfecta de Incentivos:**
- Plataforma gana cuando usuarios completan intercambios satisfactorios
- No hay conflicto de interés con publicidad
- Modelo escala con satisfacción usuario

### Ventajas de Sostenibilidad

**1. Impacto Medioambiental Cuantificable:**
- Extensión vida útil productos: 3-5 años adicionales
- Reducción residuos: ~150kg CO2 equivalente por transacción
- Economía circular real vs greenwashing

**2. Impacto Social:**
- Acceso a bienes sin necesidad de liquidez
- Reducción desigualdades económicas
- Construcción de comunidades locales
- Fomento de confianza entre ciudadanos

**3. Contribución a ODS (Objetivos Desarrollo Sostenible):**
- ODS 12: Producción y consumo responsables
- ODS 13: Acción por el clima
- ODS 11: Ciudades y comunidades sostenibles

### Barreras de Entrada

**1. Complejidad Algorítmica:**
- Matching de grafos no trivial
- Optimización económica compleja
- Sistema reputación sofisticado
- **Tiempo desarrollo estimado:** 6-9 meses equipo especializado

**2. Efecto Red Local:**
- Comunidades geográficas requieren masa crítica
- Confianza entre usuarios es acumulativa
- **Ventaja primer mover:** difícil de replicar una vez establecido

**3. Base de Datos de Preferencias:**
- Historial de transacciones exitosas
- Patrones de comportamiento usuario
- Valoraciones y reputaciones
- **Activo intangible valioso** que crece con el tiempo

---

## 5. MODELO DE NEGOCIO Y PROYECCIONES FINANCIERAS

### Flujos de Ingresos Multicapa

**Fase 1 (Año 1 - Lanzamiento): Comisión Básica 1%**
- Aplicada sobre valor del artículo adquirido
- Pagada exclusivamente por el usuario que recibe el bien
- Ejemplo: Recibe artículo valor 500€ → paga 5€ comisión
- **Justificación:** Competitividad extrema vs 5-15% competencia

**Fase 2 (Año 2 - Crecimiento): Servicios Premium**
- **Cuenta Verificada:** 4,99€/mes (verificación identidad + badge)
- **Destacados en Búsquedas:** 2,99€/artículo (mayor visibilidad)
- **Logística Premium:** +3€/envío (seguimiento avanzado + seguro)
- **Objetivo penetración:** 20% usuarios premium año 2

**Fase 3 (Año 3 - Madurez): Publicidad Segmentada**
- **Anuncios marcas sostenibles:** Empresas con certificación B Corp
- **Promociones categorías específicas:** Ej: "moda sostenible primavera"
- **Partnerships empresas circulares:** Plataformas reparación, upcycling, etc.
- **Modelo:** CPM (coste por mil impresiones) + CPC (coste por clic)

### Inversión Inicial Detallada (58.000€)

**Desarrollo Tecnológico (23.200€ - 40%):**
- Frontend Next.js/React (3 meses): 8.000€
- Backend Node.js/Python (3 meses): 7.500€
- Algoritmos matching (2 meses): 4.200€
- Infraestructura cloud (12 meses): 3.500€

**Marketing Inicial (20.300€ - 35%):**
- Campañas digitales Google/Facebook: 9.000€
- Contenido + SEO + blog: 5.300€
- Eventos lanzamiento Barcelona: 6.000€

**Operaciones y Equipo (14.500€ - 25%):**
- Equipo fundador (3 personas × 6 meses media jornada): 9.000€
- Legal + administrativo (SL, contratos, protección IP): 3.500€
- Oficina coworking + herramientas software: 2.000€

### Financiación Propuesta

**Estructura óptima:**
- **40.000€ (69%):** Inversores ángeles / business angels
- **10.000€ (17%):** Préstamo participativo ENISA
- **8.000€ (14%):** Aportación equipo fundador (trabajo + capital)

**Valoración pre-money:** 200.000€
**Equity ofrecido:** 15-20% (dependiendo experiencia equipo)
**ROI esperado inversores:** 3-5x en 3-5 años

### Proyecciones Financieras 2026-2029

**Supuestos clave:**
- Comisión efectiva: 1% sobre valor artículo adquirido
- Valor medio transacción: 150€ (año 1), 160€ (año 2), 170€ (año 3)
- Tasa conversión usuarios activos → transacciones: 10% mensual
- Crecimiento usuarios: 15% mensual (año 1), 10% (año 2), 5% (año 3)
- Retención mensual usuarios: 70%

**Proyecciones Anuales:**

| Métrica | Año 1 (2026-27) | Año 2 (2027-28) | Año 3 (2028-29) |
|---------|-----------------|-----------------|-----------------|
| **Usuarios activos finales** | 25.000 | 75.000 | 150.000 |
| **Transacciones anuales** | 15.000 | 60.000 | 120.000 |
| **Volumen transaccional** | 2.250.000€ | 9.000.000€ | 18.000.000€ |
| **Ingresos comisiones (1%)** | 22.500€ | 90.000€ | 180.000€ |
| **Ingresos servicios premium** | 0€ | 18.000€ | 48.000€ |
| **Ingresos publicidad** | 0€ | 6.000€ | 18.000€ |
| **TOTAL INGRESOS** | **22.500€** | **114.000€** | **246.000€** |

**Estado de Pérdidas y Ganancias Proyectado:**

| Concepto | Año 1 | Año 2 | Año 3 |
|----------|-------|-------|-------|
| **Ingresos totales** | 22.500€ | 114.000€ | 246.000€ |
| **Costes desarrollo** | (23.200€) | (25.000€) | (30.000€) |
| **Costes marketing** | (20.300€) | (35.000€) | (45.000€) |
| **Costes personal** | (9.000€) | (18.000€) | (30.000€) |
| **Costes operativos** | (5.500€) | (8.000€) | (12.000€) |
| **EBITDA** | **(35.500€)** | **28.000€** | **129.000€** |
| **Amortizaciones** | (1.000€) | (1.500€) | (2.000€) |
| **Intereses financieros** | (500€) | (1.000€) | (1.500€) |
| **Resultado antes impuestos** | **(