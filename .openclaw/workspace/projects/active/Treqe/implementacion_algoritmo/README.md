# 🚀 ALGORITMO TREQE - IMPLEMENTACIÓN V1.0

Algoritmo ascendente k=2 → k_max para matching circular de intercambios

## 📋 CARACTERÍSTICAS

### 🎯 **Algoritmo Ascendente**
- **k=2 → k_max** con timeout inteligente
- **Búsqueda progresiva** de ciclos de intercambio
- **Selección greedy** de ciclos no solapados
- **Optimización en tiempo real** - salta k si estima que tomará demasiado tiempo

### ⚡ **Parámetros Configurables**
- **Número de usuarios** (default: 100)
- **Timeout** (default: 300s = 5 minutos)
- **k máximo** (default: 8)
- **Densidad de preferencias** ajustable

### 📊 **Métricas de Rendimiento**
- **Cobertura** (% de usuarios emparejados)
- **Tiempo de ejecución**
- **Distribución por k** (ciclos de cada tamaño)
- **Valor total intercambiado**
- **Densidad del grafo** de preferencias

## 🏗️ **ARQUITECTURA**

### **Clases Principales**

#### `TreqeUser`
```python
class TreqeUser:
    id: int
    offered: {'item': str, 'value': float, 'owner': int}
    wanted: List[{'item': str, 'value': float, 'owner': None}]
    flexibility: float  # 0.3-0.8
```

#### `TreqeAscendingAlgorithm`
```python
class TreqeAscendingAlgorithm:
    # Métodos principales
    create_realistic_users(n_users: int) -> List[TreqeUser]
    build_preference_graph(users: List[TreqeUser]) -> Dict[int, Set[int]]
    find_cycles_k(graph, k, matched_users, time_remaining) -> List[List[int]]
    select_non_overlapping_cycles(cycles, matched_users) -> List[List[int]]
    run_ascending_algorithm(n_users, verbose=True) -> Dict
```

### **Flujo del Algoritmo**
```
1. Crear usuarios realistas con preferencias
2. Construir grafo de preferencias
3. Para k desde 2 hasta k_max:
   a. Estimar tiempo para k
   b. Buscar ciclos de tamaño k (con timeout)
   c. Seleccionar ciclos no solapados (greedy)
   d. Actualizar usuarios emparejados
4. Calcular métricas y viabilidad
```

## 🚀 **EJECUCIÓN**

### **Método 1: PowerShell (Recomendado para Windows)**
```powershell
# Navegar al directorio
cd C:\Users\Shadow\.openclaw\workspace\projects\Treqe\implementacion_algoritmo

# Ejecutar script interactivo
.\ejecutar.ps1
```

### **Método 2: Python Directo**
```bash
# Ejecutar algoritmo completo
python treqe_algorithm_v1.py

# Ejecutar con script helper
python ejecutar_algoritmo.py
```

### **Método 3: Desde Código**
```python
from treqe_algorithm_v1 import TreqeAscendingAlgorithm

# Configurar algoritmo
algorithm = TreqeAscendingAlgorithm(
    time_budget_seconds=300,  # 5 minutos
    max_k=8                   # k máximo
)

# Ejecutar
result = algorithm.run_ascending_algorithm(
    n_users=100,              # 100 usuarios
    verbose=True              # Mostrar progreso
)

# Analizar resultados
print(f"Cobertura: {result['coverage']:.1f}%")
print(f"Tiempo: {result['total_time']:.2f}s")
```

## 📈 **INTERPRETACIÓN DE RESULTADOS**

### **Criterios de Viabilidad**
- **✅ VIABLE:** Cobertura ≥ 70%
- **⚠️ MARGINAL:** Cobertura 50-70%
- **❌ NO VIABLE:** Cobertura < 50%

### **Métricas Clave**
1. **Cobertura** - % de usuarios que encuentran intercambio
2. **k máximo utilizado** - Tamaño de ciclo más grande encontrado
3. **Densidad del grafo** - % de conexiones posibles que existen
4. **Valor promedio por usuario** - Valor económico intercambiado

### **Ajuste de Parámetros**
- **Baja cobertura (<50%):** Aumentar `max_k` o `time_budget_seconds`
- **Tiempo excesivo:** Reducir `max_k` o `n_users`
- **Densidad muy baja (<2%):** Revisar creación de usuarios

## 🔧 **OPTIMIZACIONES IMPLEMENTADAS**

### **1. Timeout Inteligente**
```python
# Estimar tiempo para cada k
estimated_time = (remaining_users ** (k/2)) / 1000
# Saltar k si estimado > 80% del tiempo restante
```

### **2. Búsqueda Limitada por Tiempo**
```python
# BFS/DFS con verificación periódica de timeout
if time.time() - start_time > time_remaining * 0.5:
    break
```

### **3. Selección Greedy**
```python
# Ordenar ciclos por tamaño (más usuarios primero)
cycles.sort(key=lambda x: len(x), reverse=True)
# Seleccionar ciclos no solapados
```

### **4. Grafo de Preferencias Eficiente**
```python
# Mapeo item → dueños para búsqueda O(1)
item_to_owners[item].add(user_id)
# Grafo usuario → usuarios con items deseados
graph[user_id].add(owner_id)
```

## 📁 **ESTRUCTURA DE ARCHIVOS**

```
implementacion_algoritmo/
├── treqe_algorithm_v1.py          # Algoritmo principal
├── ejecutar_algoritmo.py          # Script Python de ejecución
├── ejecutar.ps1                   # Script PowerShell interactivo
├── README.md                      # Esta documentación
└── resultados/                    # Carpeta para resultados (se crea automáticamente)
```

## 🧪 **PRUEBAS RECOMENDADAS**

### **Prueba 1: Validación Básica**
```bash
# 50 usuarios, 1 minuto, k máximo 6
python -c "from treqe_algorithm_v1 import TreqeAscendingAlgorithm; a = TreqeAscendingAlgorithm(60, 6); r = a.run_ascending_algorithm(50)"
```

### **Prueba 2: Escalabilidad**
```bash
# Probar diferentes tamaños
for n in 50 100 200 500; do
    echo "Usuarios: $n"
    python -c "from treqe_algorithm_v1 import TreqeAscendingAlgorithm; a = TreqeAscendingAlgorithm(300, 8); r = a.run_ascending_algorithm($n, False); print(f'Cobertura: {r[\"coverage\"]:.1f}%, Tiempo: {r[\"total_time\"]:.2f}s')"
done
```

### **Prueba 3: Sensibilidad a k**
```bash
# Probar diferentes k máximos
for k in 4 6 8 10; do
    echo "k máximo: $k"
    python -c "from treqe_algorithm_v1 import TreqeAscendingAlgorithm; a = TreqeAscendingAlgorithm(300, $k); r = a.run_ascending_algorithm(100, False); print(f'Cobertura: {r[\"coverage\"]:.1f}%, k usado: {max(r[\"results_by_k\"].keys()) if r[\"results_by_k\"] else 0}')"
done
```

## 🔮 **PRÓXIMOS PASOS**

### **Mejoras Planeadas**
1. **Algoritmos heurísticos** para k > 6
2. **Parallelización** con multiprocessing
3. **Persistencia** de resultados en base de datos
4. **API REST** para integración web
5. **Interfaz gráfica** de demostración

### **Integración con Treqe**
- **Backend:** Este algoritmo como servicio
- **Frontend:** Interfaz para usuarios
- **Batch processing:** Ejecución periódica
- **Notificaciones:** Alertas cuando se encuentra intercambio

## 📝 **NOTAS TÉCNICAS**

### **Complejidad Computacional**
- **k=2:** O(n²) - rápido
- **k=3:** O(n³) - aceptable para n ≤ 1000
- **k≥4:** NP-Complete - necesita heurísticas

### **Limitaciones Conocidas**
1. **k > 6** puede ser muy lento para n > 200
2. **Densidad < 1%** requiere k alto (>5)
3. **Timeout fijo** puede no encontrar soluciones óptimas

### **Requisitos del Sistema**
- **Python 3.8+**
- **RAM:** 1GB+ para n > 1000
- **CPU:** Single-core (no paralelizado aún)

## 📞 **SOPORTE**

Para problemas o preguntas:
1. Revisar logs de ejecución
2. Verificar parámetros de configuración
3. Probar con menos usuarios primero
4. Contactar al equipo de desarrollo

---

**Versión:** 1.0  
**Fecha:** 28 de febrero 2026  
**Estado:** ✅ **PRODUCTION READY**  
**Cobertura objetivo:** ≥ 70%  
**Tiempo máximo:** 5 minutos