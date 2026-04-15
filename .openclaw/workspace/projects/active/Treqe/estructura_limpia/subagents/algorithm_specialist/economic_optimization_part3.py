#!/usr/bin/env python3
"""
PARTE 3: Implementación y demostración de optimizaciones
"""

import time
import numpy as np
from typing import List, Dict, Any
import json
from dataclasses import dataclass
import numba
from numba import jit, prange, cuda
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

# ========== IMPLEMENTACIÓN CONCRETA DE OPTIMIZACIONES ==========

@dataclass
class OptimizedTreqeSystem:
    """Sistema Treqe completamente optimizado para ROI económico"""
    
    def __init__(self, n_users=100):
        self.n_users = n_users
        self.users = self._create_optimized_users(n_users)
        self.compatibility_matrix = None
        self.cache = {}
        self.performance_stats = {
            'total_cycles_processed': 0,
            'total_value_matched': 0.0,
            'total_computation_time': 0.0,
            'avg_roi': 0.0
        }
    
    def _create_optimized_users(self, n_users):
        """Crea usuarios con estructura optimizada para computación"""
        users = []
        rng = np.random.default_rng(42)  # Reproducible
        
        for i in range(n_users):
            # Distribución económica realista
            reputation = rng.beta(2, 5) * 1000  # Mayoría baja reputación
            
            # Número de items (Poisson ajustado)
            n_offered = max(1, int(rng.poisson(2.5)))
            n_desired = max(1, int(rng.poisson(3.0)))
            
            # Valores económicamente realistas
            if rng.random() < 0.15:  # 15% items premium
                offered_values = rng.uniform(500, 2000, n_offered)
                desired_values = rng.uniform(300, 1500, n_desired)
            else:  # 85% items normales
                offered_values = rng.uniform(50, 500, n_offered)
                desired_values = rng.uniform(30, 600, n_desired)
            
            users.append({
                'id': i,
                'reputation': float(reputation),
                'offered_values': offered_values.astype(np.float32),
                'desired_values': desired_values.astype(np.float32),
                'offered_mean': float(np.mean(offered_values)),
                'desired_mean': float(np.mean(desired_values)),
                'trust_multiplier': 1.0 + (reputation / 1000) * 0.2
            })
        
        return users
    
    @jit(nopython=True, parallel=True, nogil=True, cache=True)
    def build_compatibility_matrix_fast(self):
        """Construye matriz de compatibilidad ultra-rápida"""
        n = self.n_users
        compat = np.zeros((n, n), dtype=np.uint8)  # 0/1 en 8 bits
        
        # Precomputar medias para velocidad
        offered_means = np.array([u['offered_mean'] for u in self.users], dtype=np.float32)
        desired_means = np.array([u['desired_mean'] for u in self.users], dtype=np.float32)
        reputations = np.array([u['reputation'] for u in self.users], dtype=np.float32)
        
        for i in prange(n):
            rep_i = reputations[i]
            desired_mean_i = desired_means[i]
            
            for j in range(n):
                if i == j:
                    continue
                
                # Heurística económica rápida
                offered_mean_j = offered_means[j]
                rep_j = reputations[j]
                
                # 1. Diferencia de valor (económico)
                value_diff = abs(desired_mean_i - offered_mean_j) / max(desired_mean_i, offered_mean_j)
                value_score = 1.0 - min(value_diff, 0.5)
                
                # 2. Compatibilidad de reputación
                rep_diff = abs(rep_i - rep_j) / 1000.0
                rep_score = 1.0 - rep_diff * 0.3
                
                # 3. Probabilidad combinada
                prob = value_score * rep_score * 0.4  # Factor de escala
                
                # Decisión estocástica
                if np.random.random() < prob:
                    compat[i, j] = 1
        
        return compat
    
    @jit(nopython=True, parallel=True, nogil=True, cache=True)
    def find_k3_cycles_economic(self, compatibility, min_profit=10.0, max_time_ms=1000):
        """Encuentra ciclos k=3 económicamente rentables"""
        n = compatibility.shape[0]
        max_cycles = min(1000, n * 3)
        
        cycles = np.zeros((max_cycles, 3), dtype=np.int32)
        profits = np.zeros(max_cycles, dtype=np.float32)
        cycle_count = 0
        
        # Precomputar datos económicos
        offered_means = np.array([u['offered_mean'] for u in self.users], dtype=np.float32)
        reputations = np.array([u['reputation'] for u in self.users], dtype=np.float32)
        trust_mults = np.array([u['trust_multiplier'] for u in self.users], dtype=np.float32)
        
        start_time = time.perf_counter()
        
        for a in prange(n):
            # Check tiempo
            if (time.perf_counter() - start_time) * 1000 > max_time_ms:
                break
            
            # Grado de salida
            out_degree = np.sum(compatibility[a])
            if out_degree < 2:
                continue
            
            # Usuarios compatibles con a
            compat_a = np.where(compatibility[a])[0]
            
            for b in compat_a:
                # Usuarios compatibles con b (y no a)
                compat_b = np.where(compatibility[b])[0]
                valid_c = compat_b[(compat_b != a) & (compat_b != b)]
                
                for c in valid_c:
                    # Verificar ciclo a→b→c→a
                    if compatibility[c, a]:
                        # CÁLCULO ECONÓMICO RÁPIDO
                        # Valor promedio del ciclo
                        cycle_value = (offered_means[a] + offered_means[b] + offered_means[c]) / 3
                        
                        # Ajuste por reputación (confianza = menos comisiones)
                        avg_trust = (trust_mults[a] + trust_mults[b] + trust_mults[c]) / 3
                        effective_value = cycle_value * avg_trust * 3  # 3 items
                        
                        # Coste estimado de compensaciones
                        value_diff = np.std([offered_means[a], offered_means[b], offered_means[c]])
                        compensation_cost = value_diff * 0.1  # 10% del diferencial
                        
                        # Beneficio neto
                        net_profit = effective_value - compensation_cost
                        
                        if net_profit >= min_profit:
                            if cycle_count < max_cycles:
                                cycles[cycle_count] = [a, b, c]
                                profits[cycle_count] = net_profit
                                cycle_count += 1
        
        # Ordenar por profit descendente
        if cycle_count > 0:
            sorted_idx = np.argsort(-profits[:cycle_count])
            cycles[:cycle_count] = cycles[sorted_idx]
            profits[:cycle_count] = profits[sorted_idx]
        
        return cycles[:cycle_count], profits[:cycle_count]
    
    @jit(nopython=True, parallel=True, nogil=True)
    def find_k4_cycles_approximate(self, compatibility, time_budget_ms=2000, accuracy=0.8):
        """
        Algoritmo aproximado para k=4 que maximiza ROI
        Trade-off: accuracy vs speed para viabilidad económica
        """
        n = compatibility.shape[0]
        max_cycles = min(500, n * 2)
        
        cycles = np.zeros((max_cycles, 4), dtype=np.int32)
        cycle_values = np.zeros(max_cycles, dtype=np.float32)
        cycle_count = 0
        
        # Precomputar "facilidad de matching" económica
        user_scores = np.zeros(n, dtype=np.float32)
        offered_means = np.array([u['offered_mean'] for u in self.users], dtype=np.float32)
        reputations = np.array([u['reputation'] for u in self.users], dtype=np.float32)
        
        for i in range(n):
            degree = np.sum(compatibility[i])
            # Score económico: grado × valor × reputación
            user_scores[i] = degree * offered_means[i] * (1.0 + reputations[i] / 1000)
        
        # Tomar top usuarios por score económico
        threshold = np.percentile(user_scores, 100 - (accuracy * 100))
        high_value_users = np.where(user_scores >= threshold)[0]
        
        start_time = time.perf_counter()
        
        # Búsqueda limitada en usuarios de alto valor
        for idx_a in prange(len(high_value_users)):
            if cycle_count >= max_cycles:
                break
            
            # Check tiempo
            if (time.perf_counter() - start_time) * 1000 > time_budget_ms:
                break
            
            a = high_value_users[idx_a]
            
            # Conexiones de a (ordenadas por score)
            compat_a = np.where(compatibility[a])[0]
            if len(compat_a) < 2:
                continue
            
            # Ordenar conexiones por valor económico
            compat_scores = user_scores[compat_a]
            top_b_indices = np.argsort(-compat_scores)[:min(5, len(compat_a))]
            top_b = compat_a[top_b_indices]
            
            for b in top_b:
                compat_b = np.where(compatibility[b])[0]
                if len(compat_b) < 2:
                    continue
                
                # Intersección con high_value_users
                valid_c = np.intersect1d(compat_b, high_value_users)
                valid_c = valid_c[(valid_c != a) & (valid_c != b)]
                
                for c in valid_c[:3]:  # Limitar exploración
                    compat_c = np.where(compatibility[c])[0]
                    
                    # Buscar d que complete ciclo
                    possible_d = np.intersect1d(compat_c, high_value_users)
                    possible_d = possible_d[(possible_d != a) & (possible_d != b)]
                    
                    for d in possible_d[:2]:  # Limitar más
                        if compatibility[d, a]:
                            # ¡Ciclo encontrado!
                            # Valor económico estimado
                            cycle_value = (offered_means[a] + offered_means[b] + 
                                         offered_means[c] + offered_means[d]) / 4 * 4
                            
                            # Ajuste por confianza promedio
                            avg_trust = (self.users[a]['trust_multiplier'] + 
                                       self.users[b]['trust_multiplier'] + 
                                       self.users[c]['trust_multiplier'] + 
                                       self.users[d]['trust_multiplier']) / 4
                            
                            effective_value = cycle_value * avg_trust
                            
                            cycles[cycle_count] = [a, b, c, d]
                            cycle_values[cycle_count] = effective_value
                            cycle_count += 1
                            
                            if cycle_count >= max_cycles:
                                break
                    if cycle_count >= max_cycles:
                        break
                if cycle_count >= max_cycles:
                    break
            if cycle_count >= max_cycles:
                break
        
        # Ordenar por valor económico
        if cycle_count > 0:
            sorted_idx = np.argsort(-cycle_values[:cycle_count])
            cycles[:cycle_count] = cycles[sorted_idx]
            cycle_values[:cycle_count] = cycle_values[sorted_idx]
        
        return cycles[:cycle_count], cycle_values[:cycle_count]
    
    def run_economic_optimization_pipeline(self):
        """Pipeline completo de optimización económica"""
        print("\n" + "="*80)
        print("PIPELINE DE OPTIMIZACIÓN ECONÓMICA TREQE")
        print("="*80)
        
        results = {}
        
        # Paso 1: Construir matriz de compatibilidad (optimizado)
        print("\n1. Construyendo matriz de compatibilidad...")
        start = time.time()
        self.compatibility_matrix = self.build_compatibility_matrix_fast()
        build_time = time.time() - start
        density = np.sum(self.compatibility_matrix) / (self.n_users ** 2)
        print(f"   Tiempo: {build_time:.3f}s")
        print(f"   Densidad: {density:.3f} ({density*100:.1f}% pares compatibles)")
        
        # Paso 2: k=3 optimizado
        print("\n2. Ejecutando k=3 optimizado (máximo ROI)...")
        start = time.time()
        k3_cycles, k3_profits = self.find_k3_cycles_economic(
            self.compatibility_matrix, 
            min_profit=15.0,
            max_time_ms=500
        )
        k3_time = time.time() - start
        
        k3_total_value = k3_profits.sum() if len(k3_profits) > 0 else 0
        k3_avg_profit = k3_profits.mean() if len(k3_profits) > 0 else 0
        
        print(f"   Tiempo: {k3_time:.3f}s")
        print(f"   Ciclos encontrados: {len(k3_cycles)}")
        print(f"   Valor total: €{k3_total_value:.0f}")
        print(f"   Profit promedio: €{k3_avg_profit:.0f}")
        print(f"   Usuarios cubiertos: {len(set(k3_cycles.flatten()))}/{self.n_users}")
        
        # Paso 3: k=4 aproximado (si hay demanda)
        print("\n3. Ejecutando k=4 aproximado (ROI-focused)...")
        start = time.time()
        k4_cycles, k4_values = self.find_k4_cycles_approximate(
            self.compatibility_matrix,
            time_budget_ms=1000,
            accuracy=0.85
        )
        k4_time = time.time() - start
        
        k4_total_value = k4_values.sum() if len(k4_values) > 0 else 0
        k4_avg_value = k4_values.mean() if len(k4_values) > 0 else 0
        
        print(f"   Tiempo: {k4_time:.3f}s")
        print(f"   Ciclos encontrados: {len(k4_cycles)}")
        print(f"   Valor total: €{k4_total_value:.0f}")
        print(f"   Valor promedio: €{k4_avg_value:.0f}")
        print(f"   Usuarios cubiertos: {len(set(k4_cycles.flatten()))}/{self.n_users}")
        
        # Paso 4: Análisis económico comparativo
        print("\n4. ANÁLISIS ECONÓMICO COMPARATIVO:")
        print("   " + "-"*50)
        
        # Coste computacional (€)
        cost_per_second = 0.00001
        k3_cost = k3_time * cost_per_second
        k4_cost = k4_time * cost_per_second
        
        # ROI
        k3_roi = k3_total_value / k3_cost if k3_cost > 0 else 0
        k4_roi = k4_total_value / k4_cost if k4_cost > 0 else 0
        
        # Valor por usuario
        k3_users = len(set(k3_cycles.flatten())) if len(k3_cycles) > 0 else 1
        k4_users = len(set(k4_cycles.flatten())) if len(k4_cycles) > 0 else 1
        
        k3_value_per_user = k3_total_value / k3_users if k3_users > 0 else 0
        k4_value_per_user = k4_total_value / k4_users if k4_users > 0 else 0
        
        # Valor por segundo de cómputo (eficiencia)
        k3_efficiency = k3_total_value / k3_time if k3_time > 0 else 0
        k4_efficiency = k4_total_value / k4_time if k4_time > 0 else 0
        
        print(f"   Métrica              k=3              k=4")
        print(f"   {'-'*50}")
        print(f"   Tiempo (s)          {k3_time:6.3f}          {k4_time:6.3f}")
        print(f"   Coste (€)           €{k3_cost:7.5f}        €{k4_cost:7.5f}")
        print(f"   Valor total (€)     €{k3_total_value:7.0f}        €{k4_total_value:7.0f}")
        print(f"   ROI                 {k3_roi:7.1f}x         {k4_roi:7.1f}x")
        print(f"   Valor/usuario (€)   €{k3_value_per_user:7.0f}        €{k4_value_per_user:7.0f}")
        print(f"   Eficiencia (€/s)    €{k3_efficiency:7.0f}        €{k4_efficiency:7.0f}")
        print(f"   Usuarios cubiertos  {k3_users:3d}/{self.n_users}        {k4_users:3d}/{self.n_users}")
        
        # Paso