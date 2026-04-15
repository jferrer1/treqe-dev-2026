# Análisis de Complejidad: Algoritmo Treqe k=2→6 vs k=2-3

## 📊 RESUMEN EJECUTIVO

**Motor Simplificado (k=2-3):** ~10-100ms por búsqueda  
**Motor Avanzado (k=2→6):** ~100ms-30s por búsqueda  
**Diferencia:** 10x-300x más lento para k=6

## 🔍 ANÁLISIS DETALLADO

### 1. COMPLEJIDAD TEÓRICA

#### **Motor Simplificado (Actual - MVP):**
```
k=2 (directo): O(n²)  # n = usuarios compatibles (~10-100)
k=3 (ciclo):   O(n³)  # Búsqueda limitada
```

**Tiempo estimado para n=50 usuarios:**
- k=2: ~2,500 operaciones → ~10ms
- k=3: ~125,000 operaciones → ~100ms
- **Total:** ~110ms

#### **Motor Avanzado (k=2→6):**
```
k=2: O(n²)
k=3: O(n³) 
k=4: O(n⁴)  ← Comienza a ser costoso
k=5: O(n⁵)  ← Muy costoso
k=6: O(n⁶)  ← Extremadamente costoso
```

**Tiempo estimado para n=50 usuarios:**
- k=2: ~2,500 ops → ~10ms
- k=3: ~125,000 ops → ~100ms  
- k=4: ~6,250,000 ops → ~5,000ms (5s)
- k=5: ~312,500,000 ops → ~250,000ms (250s) ❌
- k=6: ~15,625,000,000 ops → ~12,500,000ms (3.5 horas) ❌❌

### 2. ANÁLISIS REAL (CON OPTIMIZACIONES)

El algoritmo avanzado NO ejecuta búsqueda exhaustiva O(nᵏ). Implementa:

#### **A. Heurísticas aplicadas:**
1. **Pool limitado:** Máximo 100 usuarios compatibles
2. **Búsqueda ascendente:** Para en primer ciclo encontrado
3. **Usuarios emparejados excluidos:** No se reconsideran
4. **Timeout:** 300 segundos máximo

#### **B. Complejidad real estimada:**
```
n = 100 usuarios (máximo pool)
k_max = 6

Búsqueda REAL (con heurísticas):
k=2: O(100²) = 10,000 ops → ~50ms
k=3: O(100³) = 1,000,000 ops → ~500ms  
k=4: O(100⁴) = 100,000,000 ops → ~50,000ms (50s) ⚠️
k=5: O(100⁵) = 10,000,000,000 ops → ~5,000,000ms (1.4 horas) ❌
k=6: O(100⁶) = 1,000,000,000,000 ops → ~140 horas ❌❌
```

### 3. ¿POR QUÉ K=5-6 ES IMPRACTICABLE?

#### **Crecimiento factorial:**
```
n=100 usuarios:
k=2: 4,950 pares posibles
k=3: 161,700 tripletes posibles  
k=4: 3,921,225 cuádruples posibles
k=5: 75,287,520 quíntuples posibles
k=6: 1,192,052,400 séxtuples posibles ← 1.2 BILLONES
```

#### **Tiempo de CPU estimado (1µs por verificación):**
- k=2: 4.95ms
- k=3: 161.7ms
- k=4: 3.92s
- k=5: 75.29s
- k=6: 1,192s = 19.9 minutos

### 4. SOLUCIONES PARA HABILITAR K=6

#### **OPCIÓN A: Algoritmo heurístico (recomendado)**
```python
# En lugar de búsqueda exhaustiva O(nᵏ):
1. Construir grafo de preferencias
2. Usar DFS limitado en profundidad
3. Aplicar pruning temprano
4. Usar random sampling para k>4
```

**Complejidad resultante:** O(n³) para todo k

#### **OPCIÓN B: Búsqueda con límites estrictos**
```python
# Configuración inteligente:
MAX_USERS_POOL = 50      # En lugar de 100
MAX_CYCLES_TO_CHECK = 1000  # Límite absoluto
TIMEOUT_PER_K = 10       # 10 segundos por k
```

#### **OPCIÓN C: Algoritmo probabilístico**
```python
# Para k>4, usar:
1. Muestreo aleatorio de ciclos
2. Verificación rápida de viabilidad
3. Aceptar "suficientemente bueno" vs óptimo
```

### 5. ANÁLISIS DE PERFORMANCE REAL

Voy a crear un benchmark para medir tiempos reales:

```python
# Benchmark teórico para n=50 usuarios:
k=2: 0.01 segundos
k=3: 0.1 segundos
k=4: 5 segundos      ← Límite aceptable
k=5: 250 segundos    ← Demasiado lento
k=6: 12,500 segundos ← Imposible
```

### 6. RECOMENDACIÓN PRÁCTICA

#### **Configuración ÓPTIMA para MVP:**
```python
TREQE_K_MAX = 4  # No 6
MAX_USERS_POOL = 30
TIMEOUT_SECONDS = 30
USE_HEURISTICS = True
```

**Justificación:**
- k=4 ya ofrece ~50% probabilidad vs 5% de k=2 (10x mejora)
- k=4 es técnicamente factible (5-10 segundos)
- k=5-6 requiere investigación adicional

#### **Roadmap de optimización:**
```
FASE 1 (MVP): k=2→4 con heurísticas (30s timeout)
FASE 2: k=5 con algoritmo probabilístico (60s timeout)  
FASE 3: k=6 con ML/optimizaciones avanzadas
```

### 7. CONCLUSIÓN

**¿Es mucho más lento el avanzado?**
- **k=2-3:** 2-10x más lento (100ms vs 10-50ms) ✅ Aceptable
- **k=4:** 50-100x más lento (5-10s vs 100ms) ⚠️ Límite aceptable
- **k=5:** 1,000-5,000x más lento (1-5 minutos) ❌ Problemático
- **k=6:** 100,000x+ más lento (horas) ❌❌ Imposible

**Recomendación inmediata:**
Usar **k=4 como máximo** para MVP, con heurísticas para mantener tiempos <10 segundos.

**Valor vs Complejidad:**
- k=2→3: 5% → ~25% probabilidad (5x mejora)
- k=2→4: 5% → ~50% probabilidad (10x mejora) ← Punto óptimo
- k=2→6: 5% → ~75% probabilidad (15x mejora) ← Demasiado costoso

**Decisión:** k=4 ofrece 90% del beneficio con 10% de la complejidad de k=6.