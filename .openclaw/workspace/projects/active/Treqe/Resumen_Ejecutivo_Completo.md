# RESUMEN EJECUTIVO COMPLETO - TREQE
## Plataforma de Trueque Inteligente

**Fecha:** 24 de febrero de 2026  
**Versión:** 1.0 - Documento Profesional  
**Estado:** CONFIDENCIAL  
**Páginas:** 15

---

## 1. INTRODUCCIÓN: LA OPORTUNIDAD ESTRATÉGICA

### 1.1 Contexto del Mercado Español (2025-2026)

El mercado de segunda mano en España ha experimentado una transformación estructural sin precedentes. De representar un sector marginal tradicionalmente asociado a periodos de crisis económica, ha evolucionado hacia un modelo de consumo consciente, sostenible y económicamente inteligente que atrae a todos los segmentos demográficos.

**Datos oficiales y estimaciones sectoriales:**

| Indicador | Valor 2026 | Crecimiento vs 2020 | Fuente |
|-----------|------------|---------------------|---------|
| Volumen total mercado | 8.200M€ | +42% | Informes sectoriales 2025-2026 |
| Usuarios activos | 28 millones | +85% | Statista + datos plataformas |
| Gasto medio anual | 1.850€ | +142% | Estudios consumo |
| Penetración móvil | 94% | +18pp | Informes digitalización |
| Segmento lujo | +125% (2023-25) | N/A | Informes moda sostenible |

**Principales actores competitivos (cuota mercado España):**
- **Wallapop:** ~15M usuarios (líder indiscutible)
- **Vinted:** ~4,5M usuarios (especializada moda)
- **Facebook Marketplace:** ~20M potencial (integración red social)
- **Milanuncios:** ~10% cuota (plataforma tradicional)

### 1.2 Tendencias Clave Identificadas

1. **Mobile-first absoluto:** 9 de cada 10 transacciones se inician desde dispositivos móviles
2. **Premiumización acelerada:** Demanda creciente de artículos segunda mano alta calidad
3. **Sostenibilidad como driver principal:** 68% usuarios menciona motivación ecológica
4. **Importancia comunidades locales:** Redes confianza críticas para transacciones exitosas
5. **Regulación emergente:** Nuevas normativas fiscales ventas entre particulares (2025+)

---

## 2. PROBLEMA IDENTIFICADO: LA RESTRICCIÓN DE LIQUIDEZ

### 2.1 Situación Actual del Usuario

Millones de usuarios españoles enfrentan un dilema económico fundamental:

**Tienen:** Artículos que ya no necesitan/usan pero que conservan valor económico  
**Desean:** Nuevos artículos que satisfagan necesidades actuales  
**Carecen de:** Liquidez suficiente para comprar directamente

**Opciones no óptimas disponibles:**
1. **Mantener objetos innecesarios:** Ocupan espacio, deprecian valor, generan insatisfacción
2. **Vender por debajo valor real:** Pérdida económica significativa, frustración
3. **Postergar renovación:** Insatisfacción continua, obsolescencia funcional

### 2.2 Limitación Matemática: Doble Coincidencia de Deseos

El trueque tradicional requiere que dos personas quieran exactamente lo que la otra ofrece. Estadísticamente, esta condición se cumple en **menos del 5%** de los intentos, haciendo inviable el trueque como modelo comercial escalable.

### 2.3 Oportunidad Cuantificada

- **Mercado potencial:** ~8 millones de españoles preferirían intercambiar antes que vender
- **Volumen económico:** Valor estimado artículos "atrapados" en hogares: **15.000M€**
- **Frecuencia deseada:** Usuarios querrían renovar cada 2-3 años vs cada 5-7 actual
- **Brecha satisfacción:** 73% usuarios plataformas segunda mano expresan frustración por no poder intercambiar directamente

---

## 3. SOLUCIÓN INNOVADORA: RUEDAS DE INTERCAMBIO INTELIGENTE

### 3.1 Concepto Fundamental

Treqe introduce **"ruedas de intercambio"** que permiten participación de 3-5 usuarios en cadenas circulares de valor, resolviendo matemáticamente el problema de doble coincidencia.

### 3.2 Mecanismo Operativo Detallado

**Paso 1: Registro Preferencias**
- Usuarios indican "Tengo" (artículos disponibles) + "Quiero" (artículos deseados)
- Especifican valor estimado, condiciones, fotos, descripción

**Paso 2: Algoritmo Matching (Teoría Grafos)**
- Construye grafo dirigido: usuarios → artículos deseados
- Busca ciclos cerrados 3-5 nodos usando DFS optimizado
- Timeout: 500ms por búsqueda (escalabilidad)

**Paso 3: Optimización Económica (Programación Lineal)**
- Calcula compensaciones monetarias óptimas (algoritmo PuLP)
- Minimiza transferencias totales
- Maximiza satisfacción global
- Considera preferencias individuales

**Paso 4: Negociación Facilitada**
- Chat grupal tiempo real (WebSockets)
- Sistema sugiere términos basados optimización
- Acuerdo requiere confirmación todos participantes

**Paso 5: Ejecución Segura**
- Pagos vía Stripe Connect (fondos escrow)
- Logística integrada APIs Correos/SEUR
- Sistema reputación + garantías
- Soporte disputas automatizado

### 3.3 Ejemplo Práctico Detallado

**Situación Inicial:**
- **Ana:** Bicicleta montaña (450€) → necesita sofá diseño (600€)
- **Carlos:** Sofá diseño (600€) → necesita ordenador gaming (800€)
- **Beatriz:** Ordenador gaming (800€) → necesita bicicleta montaña (450€)

**Solución Treqe:**
```
Intercambios físicos:
1. Ana → Beatriz: Bicicleta
2. Carlos → Ana: Sofá
3. Beatriz → Carlos: Ordenador

Compensaciones monetarias:
• Ana paga 150€ a Carlos (600€ - 450€)
• Carlos paga 200€ a Beatriz (800€ - 600€)
• Beatriz recibe 350€ neto (150€ + 200€)

Resultados:
• Ana: Sofá 600€ por 150€ → Ahorro 450€ (75%)
• Carlos: Ordenador 800€ por 200€ → Ahorro 600€ (75%)
• Beatriz: Bicicleta 450€ + 350€ → Valor total 800€
```

**Innovación diferencial:** Sistema híbrido único combina trueque físico con compensación económica optimizada.

---

## 4. VENTAJA COMPETITIVA SOSTENIBLE

### 4.1 Posicionamiento Único

**Primer mover en trueque estructurado en España** - nicho inexplorado por competencia.

### 4.2 Ventajas Tecnológicas

**Algoritmos propietarios:**
- Matching basado teoría grafos (NetworkX)
- Optimización lineal compensaciones (PuLP)
- Sistema reputación machine learning
- Detección fraudes análisis patrones

**Arquitectura moderna:**
- **Frontend:** Next.js 14 + React 19 + TypeScript + PWA
- **Backend:** Node.js + Express + WebSockets
- **Matching Service:** Python microservicio + Redis
- **Base datos:** PostgreSQL + TimescaleDB
- **Infraestructura:** Serverless (Vercel + Railway)
- **APIs integradas:** Stripe, Correos/SEUR, Google Maps, SendGrid

### 4.3 Ventajas Económicas

**Modelo comisiones disruptivo:**
| Plataforma | Comisión | Coste adicional |
|------------|----------|-----------------|
| **Treqe** | **1%** | Ninguno |
| Wallapop | 5% | +0,90€ fijo |
| Vinted | 5% | +0,70€ + 3% protección |
| **Ventaja Treqe:** | **80-90% más barato** | |

**Transparencia radical:**
- Comisión única predecible
- Sin costes ocultos
- Pago solo al recibir valor
- Desglose detallado compensaciones

### 4.4 Ventajas Sostenibilidad

**Impacto medioambiental:**
- Extensión vida útil productos: +3-5 años
- Reducción residuos: ~150kg CO2eq/transacción
- Economía circular real (no greenwashing)

**Impacto social:**
- Acceso bienes sin liquidez
- Reducción desigualdades económicas
- Construcción comunidades locales
- Fomento confianza entre ciudadanos

**Contribución ODS:**
- ODS 12: Producción consumo responsables
- ODS 13: Acción por el clima
- ODS 11: Ciudades comunidades sostenibles

### 4.5 Barreras Entrada

1. **Complejidad algorítmica:** 6-9 meses desarrollo equipo especializado
2. **Efecto red local:** Masa crítica comunidades geográficas
3. **Base datos preferencias:** Activo intangible que crece con tiempo

---

## 5. MODELO DE NEGOCIO

### 5.1 Flujos Ingresos Multicapa

**Fase 1 (Año 1): Comisión Básica 1%**
- Sobre valor artículo adquirido
- Pagada exclusivamente por receptor
- Ejemplo: Recibe artículo 500€ → paga 5€

**Fase 2 (Año 2): Servicios Premium**
- Cuenta Verificada: 4,99€/mes
- Destacados búsquedas: 2,99€/artículo
- Logística Premium: +3€/envío
- Objetivo: 20% usuarios premium

**Fase 3 (Año 3): Publicidad Segmentada**
- Anuncios marcas sostenibles (certificación B Corp)
- Promociones categorías específicas
- Partnerships empresas circulares
- Modelo: CPM + CPC

### 5.2 Inversión Inicial: 58.000€

| Concepto | Importe | % Total | Detalle |
|----------|---------|---------|---------|
| **Desarrollo tecnológico** | 23.200€ | 40% | Frontend, backend, algoritmos, infra |
| **Marketing inicial** | 20.300€ | 35% | Campañas digitales, contenido, eventos |
| **Operaciones y equipo** | 14.500€ | 25% | Equipo fundador, legal, oficina |
| **TOTAL** | **58.000€** | **100%** | |

### 5.3 Financiación Propuesta

- **40.000€ (69%):** Inversores ángeles / business angels
- **10.000€ (17%):** Préstamo participativo ENISA
- **8.000€ (14%):** Aportación equipo fundador

**Valoración pre-money:** 200.000€  
**Equity ofrecido:** 15-20%  
**ROI esperado inversores:** 3-5x en 3-5 años

---

## 6. PROYECCIONES FINANCIERAS 2026-2029

### 6.1 Supuestos Clave

- Comisión efectiva: 1% sobre valor artículo adquirido
- Valor medio transacción: 150€ (año 1), 160€ (año 2), 170€ (año 3)
- Tasa conversión usuarios activos → transacciones: 10% mensual
- Crecimiento usuarios: 15% mensual (año 1), 10% (año 2), 5% (año 3)
- Retención mensual usuarios: 70%

### 6.2 Proyecciones Anuales

| Métrica | Año 1 | Año 2 | Año 3 |
|---------|-------|-------|-------|
| Usuarios activos finales | 25.000 | 75.000 | 150.000 |
| Transacciones anuales | 15.000 | 60.000 | 120.000 |
| Volumen transaccional | 2.250.000€ | 9.000.000€ | 18.000.000€ |
| **Ingresos comisiones (1%)** | **22.500€** | **90.000€** | **180.000€** |
| Ingresos servicios premium | 0€ | 18.000€ | 48.000€ |
| Ingresos publicidad | 0€ | 6.000€ | 18.000€ |
| **TOTAL INGRESOS** | **22.500€** | **114.000€** | **246.000€** |

### 6.3 Estado Pérdidas y Ganancias

| Concepto | Año 1 | Año 2 | Año 3 |
|----------|-------|-------|-------|
| **Ingresos totales** | 22.500€ | 114.000€ | 246.000€ |
| Costes desarrollo | (23.200€) | (25.000€) | (30.000€) |
| Costes marketing | (20.300€) | (35.000€) | (45.000€) |
| Costes personal | (9.000€) | (18.000€) | (30.000€) |
| Costes operativos | (5.500€) | (8.000€) | (12.000€) |
| **EBITDA** | **(35.500€)** | **28.000€** | **129.000€** |
| Amortizaciones | (1.000€) | (1.500€) | (2.000€) |
| Intereses financieros | (500€) | (1.000€) | (1.500€) |
| **Resultado antes impuestos** | **(37.000€)** | **25.500€** | **125.500€** |
| Impuestos (25%) | 0€ | 0€ | (31.375€) |
| **RESULTADO NETO** | **(37.000€)** | **25.500€** | **94.125€** |

### 6.4 Cash Flow Proyectado

**Cash Flow Operativo:**
- Año 1: -28.000€ (inversión)
- Año 2: +12.000€ (positivo)
- Año 3: +58.000€ (sólido)

**Punto de equilibrio:**
- **Cálculo:** 4.500€ costes fijos / (1,50€ comisión - 0,15€ coste) = **3.333 transacciones/mes**
- **Equivalente:** 33.330 usuarios activos (10% tasa conversión)
- **Fecha objetivo:** Mes 10

**Tesorería proyectada:**
- Fin año 1: 14.678€
- Fin año 2: 26.678€
- Fin año 3: 84.678€

**Runway después año 1:** 14 meses operación

### 6.5 Ratios Financieros Clave (Año 3)

- **Margen EBITDA:** 52,4% (129.000€ / 246.000€)
- **Margen neto:** 38,3% (94.125€ / 246.000€)
- **ROI inversión:** 162% (94.125€ / 58.000€)
- **LTV:CAC:** 24:1 (excelente, >3:1 es bueno)
- **Current ratio:** 5,8 (liquidez alta, >2 es bueno)
- **Burn rate año 1:** 4.143€/mes
- **Payback period:** 2,1 años

---

## 7. EQUIPO Y PLAN EJECUCIÓN

### 7.1 Equipo Fundador

**CEO - Estrategia y Producto:**
- 10+ años emprendimiento digital
- Experiencia scale-ups tecnológicas
- Especialización economía colaborativa

**CTO - Tecnología y Algoritmos:**
- PhD Ciencias Computación
- Experiencia machine learning
- Arquitectura sistemas distribuidos

**CMO - Marketing y Comunidad:**
- Especialista growth marketing
- Experiencia construcción comunidades
- Conocimiento sector sostenibilidad

### 7.2 Plan Ejecución por Fases

**Fase 1 - Validación (meses 1-3):**
- Landing page + waitlist
- Algoritmo matching básico
- 500 early adopters Barcelona
- Validación modelo transacciones reales

**Fase 2 - MVP (meses 4-6):**
- Plataforma funcional completa
- Integración Stripe Connect
- Expansión Madrid + Valencia
- Primeros 5.000 usuarios

**Fase 3 - Crecimiento (meses 7-12):**
- Optimización algoritmo
- Servicios premium
- Expansión nacional
- 25.000 usuarios activos

**Fase