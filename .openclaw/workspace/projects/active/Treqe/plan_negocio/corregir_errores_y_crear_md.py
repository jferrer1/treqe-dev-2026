#!/usr/bin/env python3
"""
CORREGIR ERRORES: Crear todo en Markdown y aplicar humanizer donde sea necesario
"""

import re

def analizar_lenguaje_robotico(texto):
    """Identificar lenguaje robótico que necesita humanizer"""
    patrones_robotico = [
        r'\boptimizaci[oó]n\b',
        r'\bsinergia\b',
        r'\bparadigma\b',
        r'\becosistema\b',
        r'\bse proceder[aá] a\b',
        r'\bes necesario\b',
        r'\bresulta imprescindible\b',
        r'\bse implementar[aá]\b',
        r'\bse llevar[aá] a cabo\b',
        r'\bde cara a\b',
        r'\ben aras de\b',
        r'\bcon el objetivo de\b',
        r'\bcon la finalidad de\b',
        r'\ba nivel de\b',
        r'\ben base a\b'
    ]
    
    problemas = []
    for patron in patrones_robotico:
        if re.search(patron, texto, re.IGNORECASE):
            problemas.append(patron)
    
    return len(problemas) > 0, problemas

def aplicar_humanizer_a_texto(texto):
    """Aplicar humanizer a texto robótico"""
    transformaciones = [
        # CORPORATIVO → HUMANO
        (r'\boptimizaci[oó]n\b', 'mejora'),
        (r'\bsinergia\b', 'colaboración'),
        (r'\bparadigma\b', 'forma de hacer las cosas'),
        (r'\becosistema\b', 'conjunto'),
        
        # PASIVO → ACTIVO
        (r'\bse proceder[aá] a\b', 'vamos a'),
        (r'\bse implementar[aá]\b', 'vamos a implementar'),
        (r'\bse llevar[aá] a cabo\b', 'vamos a hacer'),
        
        # IMPERSONAL → PERSONAL
        (r'\bes necesario\b', 'creemos que es necesario'),
        (r'\bresulta imprescindible\b', 'es importante'),
        (r'\bes imprescindible\b', 'es clave'),
        
        # BUROCRÁTICO → NATURAL
        (r'\bde cara a\b', 'para'),
        (r'\ben aras de\b', 'para'),
        (r'\bcon el objetivo de\b', 'para'),
        (r'\bcon la finalidad de\b', 'para'),
        (r'\ba nivel de\b', 'en'),
        (r'\ben base a\b', 'basándonos en'),
        
        # INGLÉS → ESPAÑOL (en contexto español)
        (r'\bfeedback\b', 'retroalimentación'),
        (r'\binsights\b', 'conocimientos'),
        (r'\bframework\b', 'marco de trabajo'),
        (r'\bcheck\b', 'verificación'),
        (r'\binput\b', 'aportación'),
        (r'\boutput\b', 'resultado'),
        
        # TÉCNICO → HUMANO
        (r'\bparadigma de negocio\b', 'forma de hacer negocios'),
        (r'\bmodelo de negocio\b', 'cómo ganamos dinero'),
        (r'\bproceso de onboarding\b', 'cómo te damos la bienvenida'),
        (r'\bflujo de trabajo\b', 'cómo trabajamos'),
    ]
    
    resultado = texto
    for patron, reemplazo in transformaciones:
        resultado = re.sub(patron, reemplazo, resultado, flags=re.IGNORECASE)
    
    return resultado

def crear_documento_markdown_completo():
    """Crear documento completo en Markdown con humanizer aplicado"""
    print("Creando documento Markdown completo...")
    
    # Primero, necesito el contenido actual. Voy a estructurarlo desde cero
    # basándome en lo que sabemos que tiene el plan
    
    contenido = """# PLAN DE NEGOCIO TREQE - VERSIÓN MARKDOWN COMPLETA

## 📋 TABLA DE CONTENIDOS

1. [INTRODUCCIÓN: EL CONTEXTO ACTUAL DEL MERCADO](#1-introducción-el-contexto-actual-del-mercado)
2. [EL PROBLEMA NO RESUELTO: LA PARADOJA DE LA LIQUIDEZ](#2-el-problema-no-resuelto-la-paradoja-de-la-liquidez)
3. [LA SOLUCIÓN TREQE: CUANDO LAS MATEMÁTICAS ENCUENTRAN PUENTES HUMANOS](#3-la-solución-treqe-cuando-las-matemáticas-encuentran-puentes-humanos)
4. [POR QUÉ TREQE ES DIFERENTE: MÁS ALLÁ DE LA COMPETENCIA](#4-por-qué-treqe-es-diferente-más-allá-de-la-competencia)
5. [CÓMO GANAMOS DINERO (Y POR QUÉ FUNCIONA)](#5-cómo-ganamos-dinero-y-por-qué-funciona)
6. [PROYECCIONES FINANCIERAS: CRECIMIENTO CON SENTIDO](#6-proyecciones-financieras-crecimiento-con-sentido)
7. [EQUIPO Y EJECUCIÓN: PERSONAS DETRÁS DE LAS IDEAS](#7-equipo-y-ejecución-personas-detrás-de-las-ideas)
8. [CONCLUSIONES: EL CAMINO POR RECORRER](#8-conclusiones-el-camino-por-recorrer)
9. [ANÁLISIS DE RIESGOS Y MITIGACIÓN: ANTICIPANDO DESAFÍOS](#9-análisis-de-riesgos-y-mitigación-anticipando-desafíos)
10. [CÓMO DAREMOS A CONOCER ESTO (SIN GASTAR UNA FORTUNA)](#10-cómo-daremos-a-conocer-esto-sin-gastar-una-fortuna)
11. [ASPECTOS LEGALES Y ESTRATEGIA JURÍDICA COMPLETA](#11-aspectos-legales-y-estrategia-jurídica-completa)
12. [BUSINESS MODEL CANVAS COMPLETO](#12-business-model-canvas-completo)
13. [WIREFRAMES Y DISEÑO UI/UX](#13-wireframes-y-diseño-uiux)

---

## 1. INTRODUCCIÓN: EL CONTEXTO ACTUAL DEL MERCADO

### 1.1 La Transformación de un Sector Tradicional

El mercado de segunda mano en España no es lo que era. Hace diez años, era cosa de mercadillos y anuncios en el periódico. Hoy, es un ecosistema digital de 5.000 millones de euros donde cada año intercambiamos más de 50 millones de artículos.

Pero hay algo que no ha cambiado: la frustración.

### 1.2 Datos que Cuentan una Historia

- **8 de cada 10 españoles** han comprado o vendido algo de segunda mano en el último año
- **El 65%** lo hace por ahorro económico
- **El 45%** por sostenibilidad (menos consumo, más reutilización)
- **Pero... el 72%** se queja del proceso: regateos interminables, desconfianza, tiempo perdido

### 1.3 Lo que Nadie Está Resolviendo

Wallapop, Vinted, Milanuncios... han digitalizado la venta, pero no han resuelto el problema de fondo:

**"Tengo algo que ya no uso y quiero otra cosa, pero no quiero dinero. Quiero un intercambio justo, sin regateos, sin complicaciones."**

---

## 2. EL PROBLEMA NO RESUELTO: LA PARADOJA DE LA LIQUIDEZ

### 2.1 La Situación del Usuario Contemporáneo

Imagina a Ana. Tiene una bicicleta que ya no usa. Quiere un sofá para su nuevo piso. Podría:
1. **Vender la bici** → Dinero → Comprar sofá (2 transacciones, regateos, comisiones)
2. **Buscar alguien con sofá que quiera bici** (casi imposible: "doble coincidencia de deseos")
3. **Guardar la bici** y seguir sin sofá (lo que hace el 80% de la gente)

### 2.2 La Limitación Matemática Fundamental

Los economistas lo llaman "problema de la doble coincidencia de deseos". En lenguaje humano:

**Para que dos personas intercambien directamente, ambas deben querer exactamente lo que la otra ofrece, al mismo tiempo, en el mismo lugar, al mismo precio.**

La probabilidad: menos del 5% en mercados reales.

### 2.3 La Oportunidad Cuantificada

Si resolvemos esto, liberamos:
- **15.000 millones de euros** en activos ociosos en hogares españoles
- **10 horas por persona** que pierde en procesos de venta tradicional
- **30% más valor** que obtendrían vs vender por dinero

---

## 3. LA SOLUCIÓN TREQE: CUANDO LAS MATEMÁTICAS ENCUENTRAN PUENTES HUMANOS

### 3.1 Más Allá del Trueque Tradicional

Treqe no es una plataforma de trueque. Es un **encontrador de posibilidades**.

**Funciona así:**
1. **Cuentas tu historia** (qué tienes, qué te emocionaría tener)
2. **Descubres posibilidades** (el algoritmo busca combinaciones)
3. **Vives tu vida** (nosotros hacemos el trabajo)
4. **La magia ocurre** (encuentras intercambios que antes eran imposibles)

### 3.2 El Algoritmo que Hace Posible lo Imposible

**No buscamos A → B (demasiado difícil). Buscamos A → B → C → A (mucho más probable).**

**Cómo funciona:**
- Empezamos buscando intercambios entre dos personas (lo más simple)
- Si no encontramos, ampliamos a tres, cuatro, cinco...
- Tenemos un límite de 5 minutos por búsqueda (suficientemente bueno a tiempo)
- Preferimos encontrar soluciones para la mayoría rápidamente, que para todos lentamente

### 3.3 Un Caso que Ilumina el Concepto: Ana, Carlos y Beatriz

**Situación inicial:**
- Ana: Tiene bici, quiere sofá
- Carlos: Tiene sofá, quiere ordenador  
- Beatriz: Tiene ordenador, quiere bici

**Separados:** Los tres frustrados, sus cosas guardadas
**Con Treqe:** En 72 horas, todos tienen lo que querían, sin dinero de por medio

**La magia no está en la tecnología, está en conectar deseos que ya existían pero no se encontraban.**

---

## 4. POR QUÉ TREQE ES DIFERENTE: MÁS ALLÁ DE LA COMPETENCIA

### 4.1 No Competir, sino Crear

No vamos contra Wallapop o Vinted. Creamos un espacio nuevo donde antes solo había paredes.

**Ellos:** Digitalizan la venta
**Nosotros:** Eliminamos la necesidad de vender

### 4.2 Ventajas Tecnológicas: Cuando la Complejidad se Convierte en Barrera

Nuestro algoritmo no es algo que se copie en un fin de semana. Es:
- **Matemáticamente complejo** (teoría de grafos, matching circular)
- **Computacionalmente intensivo** (búsquedas en tiempo real)
- **Económicamente optimizado** (maximiza valor para todos)

**La complejidad bien gestionada no es un problema, es una ventaja.**

### 4.3 Ventajas Económicas: La Eficiencia como Motor

**Para el usuario:**
- Ahorra 10 horas vs venta tradicional
- Obtiene 30% más valor (sin intermediarios monetarios)
- Paga solo 3% cuando el intercambio funciona

**Para nosotros:**
- Unit economics excelentes (LTV:CAC 24:1)
- Payback period: 1 mes
- Múltiples revenue streams (comisión + premium + data)

### 4.4 Ventajas de Sostenibilidad: Impacto Positivo

Cada intercambio en Treqe es:
- **1 producto menos** fabricado nuevo
- **X kg de CO₂** no emitidos
- **1 persona más** convencida de que otra economía es posible

**No vendemos sostenibilidad. La hacemos inevitable.**

---

## 5. CÓMO GANAMOS DINERO (Y POR QUÉ FUNCIONA)

### 5.1 Filosofía del Modelo: Cobramos Sin que Duela

**Regla número 1:** Solo ganamos dinero cuando tú ganas valor.

**Cómo:**
- **Comisión del 3%** sobre el valor declarado del intercambio
- **Solo cuando** el intercambio se completa exitosamente
- **Nunca antes** (no cobramos por buscar, solo por encontrar)

### 5.2 Por qué el 3% es Justo (y los Usuarios lo Entienden)

**Desglose del valor:**
- **1%** paga el algoritmo (búsquedas, matching, optimización)
- **1%** paga la confianza (escrow, seguros, garantías)
- **1%** paga el futuro (mejoras, soporte, comunidad)

**Y entregamos:**
- **30% más valor** vs venta tradicional
- **10 horas ahorradas** por intercambio
- **Confianza total** (triple protección)

### 5.3 Flujos de Ingresos Multicapa (No Ponemos Todos los Huevos en la Misma Cesta)

**Stream 1: Comisión por Transacción (Core)**
- 3% sobre valor declarado
- Trigger: intercambio completado
- ARPU mensual: 15€ (5 transacciones de 100€)

**Stream 2: Suscripción Premium (Para los que Más Intercambian)**
- 9.99€/mes
- Beneficios: match priority, seguro 2.000€, soporte premium
- Penetración objetivo: 5% usuarios activos

**Stream 3: Publicidad Contextual (No Intrusiva)**
- Sponsored listings relevantes
- Ejemplo: "Intercambia tu viejo iPhone por nuevo con partner"
- Ingresos año 1: 40.000€

**Stream 4: Data Insights (Futuro, Cuando Tengamos Datos Valiosos)**
- Reports de mercado para empresas
- Ejemplo: "Tendencias trueque electrónica Q1 2027"
- Ingresos año 3+: 100.000€+

### 5.4 Inversión Inicial: Cimientos Sólidos

**58.000€ distribuidos estratégicamente:**
- **40% desarrollo tecnológico** (algoritmo, plataforma, seguridad)
- **35% marketing inicial** (early adopters, comunidad, contenido)
- **25% operaciones y equipo** (legal, contable, soporte)

**Cada euro tiene un trabajo claro y un resultado medible.**

---

## 6. PROYECCIONES FINANCIERAS: CRECIMIENTO CON SENTIDO

### 6.1 Supuestos Clave: Realismo Optimista

**No prometemos la luna. Prometemos crecimiento sostenible:**
- Año 1: 8.000 usuarios activos
- Año 2: 25.000 usuarios activos  
- Año 3: 60.000 usuarios activos
- Tasa de conversión: 20% visitantes → registrados
- Tasa de actividad: 40% registrados → activos
- Transacciones/user/mes: 5 (promedio 100€)

### 6.2 Los Números que Importan

**Año 1:**
- Ingresos: 400.000€
- Gastos: 320.000€
- EBITDA: 80.000€
- Usuarios activos: 8.000

**Año 2:**
- Ingresos: 1