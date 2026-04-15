# Problema de Optimización: Ruedas de Intercambio Treqe

## Descripción del Problema

**Contexto:** Treqe es un marketplace de intercambio de segunda mano donde usuarios intercambian items con compensaciones monetarias.

**Problema:** Encontrar "ruedas de intercambio" circulares donde:
- Cada usuario ofrece 1+ items
- Cada usuario desea 1+ items de otros usuarios
- Se forma un ciclo dirigido: A→B→C→...→A
- Se calculan compensaciones monetarias basadas en:
  - Diferencia de valor entre items
  - Nivel de reputación del usuario (Novato, Miembro, Confiable, Elite)
  - Comisiones por nivel (1.0%, 0.9%, 0.8%)

**Objetivo:** Optimizar el algoritmo para manejar ruedas más grandes (k > 3 usuarios) manteniendo viabilidad computacional.

## Análisis Técnico Actual

### Complejidad Identificada:
- **Problema NP-Completo:** Encontrar ciclos Hamiltonianos de tamaño k
- **Crecimiento factorial:** k=4 es ~100x más lento que k=3 para 100 usuarios
- **Datos concretos para 100 usuarios:**
  - k=2: 4,950 combinaciones → 5ms
  - k=3: 161,700 combinaciones → 1.6s  
  - k=4: 3,921,225 combinaciones → 6.5 minutos
  - k=5: 75,287,520 combinaciones → ~21 horas
  - k=6: 1,192,052,400 combinaciones → ~138 días

### Limitaciones Actuales:
1. **Algoritmo greedy simple:** Solo encuentra matches directos 1:1
2. **Búsqueda exhaustiva:** Imposible para k>3 con muchos usuarios
3. **No considera heurísticas:** Podría encontrar soluciones subóptimas pero rápidas

## Requisitos de Optimización

### Objetivos:
1. **Manejar k=4-6 usuarios** de manera práctica
2. **Mantener tiempo de ejecución <10s** para 100 usuarios
3. **Encontrar soluciones "suficientemente buenas"** (no necesariamente óptimas)
4. **Incorporar sistema de reputación** en compensaciones
5. **Ser escalable** hasta 1000+ usuarios

### Restricciones:
- **Preservar equidad:** Compensaciones justas basadas en reputación
- **Mantener simplicidad:** Experiencia usuario comprensible
- **Garantizar viabilidad:** Algoritmo implementable en producción

## Enfoques de Optimización a Considerar

### 1. **Heurísticas Greedy con Búsqueda Limitada**
- Buscar ciclos incrementalmente (2→3→4 usuarios)
- Limitar búsqueda a usuarios con preferencias similares
- Usar pruning temprano basado en valor/reputación

### 2. **Algoritmos de Aproximación para Ciclo Hamiltoniano**
- Algoritmos de Christofides (para grafos métricos)
- Algoritmos de inserción (nearest neighbor, cheapest insertion)
- Algoritmos genéticos para optimización combinatoria

### 3. **Descomposición del Problema**
- Dividir usuarios en clusters por categorías/locación
- Resolver ciclos dentro de cada cluster
- Conectar clusters con intercambios puente

### 4. **Machine Learning para Predicción**
- Predecir matches probables basados en historial
- Buscar solo en pares con alta probabilidad de match
- Aprender patrones de preferencias de usuarios

### 5. **Computación Distribuida**
- Paralelizar búsqueda de ciclos
- Usar MapReduce para combinaciones
- Cachear resultados intermedios

## Métricas de Éxito

### Primarias:
- **Tasa de matching:** >40% usuarios emparejados
- **Tiempo ejecución:** <5s para 100 usuarios, <30s para 1000
- **Valor intercambiado:** Maximizar €/usuario
- **Satisfacción:** >70% usuarios satisfechos

### Secundarias:
- **Complejidad implementación:** Mantener razonable
- **Escalabilidad:** Funcionar con 10k+ usuarios
- **Robustez:** Manejar casos límite y fallos

## Próximos Pasos

1. **Implementar heurísticas greedy** para k=4
2. **Probar algoritmos de aproximación** (Christofides, insertion)
3. **Evaluar ML para predicción** de matches
4. **Diseñar arquitectura distribuida** si necesario
5. **Validar con datos reales/simulados**

## Preguntas Clave para Algorithm-Solver

1. ¿Cuáles son los mejores algoritmos de aproximación para encontrar ciclos Hamiltonianos en grafos dirigidos con pesos?

2. ¿Cómo podemos incorporar restricciones adicionales (reputación, compensaciones) en estos algoritmos?

3. ¿Qué heurísticas funcionan mejor para pruning temprano en búsqueda combinatoria?

4. ¿Cómo balancear optimalidad vs velocidad en problemas NP-Completos prácticos?

5. ¿Qué técnicas de ML son más efectivas para predecir matches en sistemas de recomendación?