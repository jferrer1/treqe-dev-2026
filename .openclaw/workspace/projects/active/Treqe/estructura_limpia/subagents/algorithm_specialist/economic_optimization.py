#!/usr/bin/env python3
"""
OPTIMIZACIÓN ECONÓMICA del algoritmo Treqe
Objetivo: Maximizar € por ciclo computacional
"""

import time
import random
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from enum import Enum
import numba
from numba import jit, prange
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

# ========== CONFIGURACIÓN ECONÓMICA ==========

COST_CPU_PER_SECOND = 0.00001  # €/s (coste aproximado de computación)
MIN_ROI_RATIO = 2.0  # ROI mínimo aceptable (2x retorno por coste computacional)

# ========== ESTRUCTURAS OPTIMIZADAS ==========

@dataclass
class EconomicUser:
    """Usuario optimizado para cálculo económico"""
    id: int
    reputation: float  # 0-1000
    offered_values: np.ndarray  # Valores de items ofrecidos
    desired_values: np.ndarray  # Valores de items deseados
    offered_ids: np.ndarray     # IDs de items ofrecidos
    desired_ids: np.ndarray     # IDs de items deseados
    
    @property
    def commission_rate(self) -> float:
        """Comisión basada en reputación (mejor reputación = menor comisión)"""
        return max(0.005, 0.01 - (self.reputation / 1000) * 0.005)
    
    @property
    def trust_multiplier(self) -> float:
        """Multiplicador de confianza para compensaciones"""
        return 1.0 + (self.reputation / 1000) * 0.2

# ========== ALGORITMO OPTIMIZADO CON NUMBA ==========

@jit(nopython=True, parallel=True, nogil=True)
def find_profitable_k3_cycles_numba(
    n_users: int,
    compatibility: np.ndarray,      # Matriz booleana n×n
    offered_values: np.ndarray,     # n×max_items
    desired_values: np.ndarray,     # n×max_items  
    reputations: np.ndarray,        # n
    min_profit_per_cycle: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Encuentra ciclos k=3 económicamente rentables usando GPU-like optimizations
    """
    max_cycles = n_users * 10  # Límite razonable
    cycles = np.zeros((max_cycles, 3), dtype=np.int32)
    profits = np.zeros(max_cycles, dtype=np.float32)
    cycle_count = 0
    
    # Precomputar comisiones por usuario
    commissions = 0.01 - (reputations / 1000) * 0.005
    commissions = np.maximum(commissions, 0.005)
    
    # Búsqueda optimizada con pruning económico
    for a in prange(n_users):
        if cycle_count >= max_cycles:
            break
            
        # Solo usuarios con al menos 2 conexiones salientes
        out_degree = np.sum(compatibility[a])
        if out_degree < 2:
            continue
            
        # Obtener usuarios compatibles con a
        compatible_with_a = np.where(compatibility[a])[0]
        
        for b_idx in range(len(compatible_with_a)):
            b = compatible_with_a[b_idx]
            
            # b debe tener conexión a algún c
            compatible_with_b = np.where(compatibility[b])[0]
            
            for c in compatible_with_b:
                if c == a or c == b:
                    continue
                    
                # Verificar ciclo a→b→c→a
                if compatibility[c, a]:
                    # CALCULAR RENTABILIDAD ECONÓMICA
                    # Valor intercambiado aproximado
                    avg_value = (np.mean(offered_values[a]) + 
                                np.mean(offered_values[b]) + 
                                np.mean(offered_values[c])) / 3
                    
                    # Coste de compensaciones (simplificado)
                    compensation_cost = 0.0
                    
                    # Ajustar por reputación
                    trust_avg = (reputations[a] + reputations[b] + reputations[c]) / 3000
                    effective_value = avg_value * (1.0 + trust_avg * 0.1)
                    
                    # Coste de comisiones
                    commission_cost = effective_value * (commissions[a] + commissions[b] + commissions[c])
                    
                    # Beneficio neto
                    net_profit = effective_value - commission_cost - compensation_cost
                    
                    # Solo si es rentable
                    if net_profit >= min_profit_per_cycle:
                        if cycle_count < max_cycles:
                            cycles[cycle_count] = [a, b, c]
                            profits[cycle_count] = net_profit
                            cycle_count += 1
    
    return cycles[:cycle_count], profits[:cycle_count]

@jit(nopython=True)
def find_high_roi_k4_approximate(
    n_users: int,
    compatibility: np.ndarray,
    values: np.ndarray,
    reputations: np.ndarray,
    time_budget_ms: float
) -> np.ndarray:
    """
    Algoritmo aproximado para k=4 que MAXIMIZA ROI
    Trade-off: 80-90% optimalidad por 10-100x speedup
    """
    max_cycles = 1000
    cycles = np.zeros((max_cycles, 4), dtype=np.int32)
    cycle_values = np.zeros(max_cycles, dtype=np.float32)
    cycle_count = 0
    
    start_time = time.perf_counter()
    
    # Estrategia: Buscar ciclos "fáciles" primero (alto ROI)
    # 1. Ordenar usuarios por "facilidad de matching" (grado × reputación)
    user_scores = np.zeros(n_users, dtype=np.float32)
    for i in range(n_users):
        degree = np.sum(compatibility[i])
        user_scores[i] = degree * (1.0 + reputations[i] / 1000)
    
    # Tomar top 30% usuarios (los más "matchables")
    threshold = np.percentile(user_scores, 70)
    high_score_users = np.where(user_scores >= threshold)[0]
    
    # Búsqueda limitada en este subconjunto
    for idx_a in range(len(high_score_users)):
        if cycle_count >= max_cycles:
            break
            
        # Check tiempo
        if (time.perf_counter() - start_time) * 1000 > time_budget_ms:
            break
            
        a = high_score_users[idx_a]
        
        # Solo conexiones de alta compatibilidad
        compatible_a = np.where(compatibility[a])[0]
        if len(compatible_a) < 2:
            continue
            
        # Ordenar por score descendente
        compatible_scores = user_scores[compatible_a]
        sorted_indices = np.argsort(-compatible_scores)
        
        # Tomar solo top 5 conexiones
        top_b = compatible_a[sorted_indices[:5]]
        
        for b in top_b:
            compatible_b = np.where(compatibility[b])[0]
            if len(compatible_b) < 2:
                continue
                
            # Intersección con high_score_users
            valid_c = np.intersect1d(compatible_b, high_score_users)
            valid_c = valid_c[valid_c != a]
            
            for c in valid_c[:3]:  # Limitar a 3 opciones
                compatible_c = np.where(compatibility[c])[0]
                
                # Buscar d que complete el ciclo y esté en high_score_users
                possible_d = np.intersect1d(compatible_c, high_score_users)
                possible_d = possible_d[(possible_d != a) & (possible_d != b)]
                
                for d in possible_d[:2]:  # Limitar a 2 opciones
                    if compatibility[d, a]:
                        # ¡Ciclo encontrado!
                        # Calcular valor aproximado
                        cycle_value = np.mean([
                            np.mean(values[a]), np.mean(values[b]),
                            np.mean(values[c]), np.mean(values[d])
                        ]) * 4  # Aproximación
                        
                        cycles[cycle_count] = [a, b, c, d]
                        cycle_values[cycle_count] = cycle_value
                        cycle_count += 1
                        
                        if cycle_count >= max_cycles:
                            break
                if cycle_count >= max_cycles:
                    break
            if cycle_count >= max_cycles:
                break
        if cycle_count >= max_cycles:
            break
    
    # Ordenar ciclos por valor descendente
    if cycle_count > 0:
        sorted_indices = np.argsort(-cycle_values[:cycle_count])
        cycles[:cycle_count] = cycles[sorted_indices]
        cycle_values[:cycle_count] = cycle_values[sorted_indices]
    
    return cycles[:cycle_count], cycle_values[:cycle_count]

# ========== SISTEMA DE DECISIÓN ECONÓMICA ==========

class EconomicDecisionSystem:
    """Sistema que decide qué tamaño de rueda usar basado en ROI"""
    
    def __init__(self, cost_cpu_per_second=COST_CPU_PER_SECOND, min_roi=MIN_ROI_RATIO):
        self.cost_cpu = cost_cpu_per_second
        self.min_roi = min_roi
        self.history = []
        
    def calculate_roi(self, total_value, computation_time, additional_costs=0):
        """Calcula ROI de un matching"""
        revenue = total_value
        cost = (computation_time * self.cost_cpu) + additional_costs
        roi = revenue / cost if cost > 0 else float('inf')
        return roi
    
    def recommend_wheel_size(self, users, market_conditions):
        """
        Recomienda tamaño óptimo de rueda basado en condiciones actuales
        """
        n_users = len(users)
        
        # Estimaciones de performance
        k3_time_est = self.estimate_k3_time(n_users)
        k4_time_est = self.estimate_k4_time(n_users)
        
        # Estimaciones de valor
        k3_value_est = self.estimate_k3_value(users)
        k4_value_est = self.estimate_k4_value(users)
        
        # Calcular ROI
        k3_roi = self.calculate_roi(k3_value_est, k3_time_est)
        k4_roi = self.calculate_roi(k4_value_est, k4_time_est)
        
        # Considerar costes adicionales
        # k4 tiene más costes de coordinación, mayor riesgo
        k4_additional_costs = k4_value_est * 0.1  # 10% costes adicionales
        k4_roi_adj = self.calculate_roi(k4_value_est, k4_time_est, k4_additional_costs)
        
        # Decisión
        recommendations = []
        
        if k3_roi >= self.min_roi:
            recommendations.append({
                'k': 3,
                'roi': k3_roi,
                'value_per_user': k3_value_est / (n_users * 0.4),  # 40% usuarios matcheados
                'computation_time': k3_time_est,
                'decision': 'STRONG_RECOMMEND' if k3_roi > k4_roi_adj * 1.5 else 'RECOMMEND'
            })
        
        if k4_roi_adj >= self.min_roi:
            recommendations.append({
                'k': 4,
                'roi': k4_roi_adj,
                'value_per_user': k4_value_est / (n_users * 0.3),  # 30% usuarios matcheados
                'computation_time': k4_time_est,
                'decision': 'CONSIDER' if k4_roi_adj < k3_roi else 'RECOMMEND'
            })
        
        # Ordenar por ROI
        recommendations.sort(key=lambda x: x['roi'], reverse=True)
        
        return recommendations
    
    def estimate_k3_time(self, n_users):
        """Tiempo estimado para k=3 con optimizaciones"""
        # O(n³) pero con optimizaciones
        base_time = 0.001  # 1ms base
        scaled_time = base_time * (n_users / 100) ** 3
        return min(scaled_time, 10.0)  # Max 10 segundos
    
    def estimate_k4_time(self, n_users):
        """Tiempo estimado para k=4 con algoritmo aproximado"""
        # Algoritmo aproximado O(n²) en vez de O(n⁴)
        base_time = 0.01  # 10ms base
        scaled_time = base_time * (n_users / 100) ** 2
        return min(scaled_time, 30.0)  # Max 30 segundos
    
    def estimate_k3_value(self, users):
        """Valor estimado para k=3"""
        avg_item_value = np.mean([np.mean(u.offered_values) for u in users])
        avg_users_matched = len(users) * 0.4  # 40% de usuarios
        return avg_item_value * avg_users_matched * 3  # 3 items por ciclo
    
    def estimate_k4_value(self, users):
        """Valor estimado para k=4 (considerando menor valor por usuario)"""
        avg_item_value = np.mean([np.mean(u.offered_values) for u in users])
        avg_users_matched = len(users) * 0.3  # 30% de usuarios (menos que k=3)
        value_per_user = avg_item_value * 0.8  # 20% menos por usuario que k=3
        return value_per_user * avg_users_matched * 4

# ========== OPTIMIZACIÓN ADAPTATIVA ==========

class AdaptiveOptimizer:
    """Optimizador que ajusta parámetros en tiempo real basado en ROI"""
    
    def __init__(self):
        self.learning_rate = 0.1
        self.parameters = {
            'k3_time_budget_ms': 1000,    # 1 segundo para k=3
            'k4_time_budget_ms': 5000,    # 5 segundos para k=4
            'min_profit_per_cycle': 10.0, # € mínimo por ciclo
            'max_cycles_to_search': 1000,
            'use_approximation': True,
            'approximation_accuracy': 0.85  # 85% optimalidad aceptable
        }
        self.performance_history = []
        
    def update_parameters(self, actual_roi, target_roi):
        """Ajusta parámetros para alcanzar target ROI"""
        roi_ratio = actual_roi / target_roi if target_roi > 0 else 1.0
        
        if roi_ratio < 0.8:  # ROI muy bajo
            # Reducir tiempo de cómputo (más aproximación)
            self.parameters['use_approximation'] = True
            self.parameters['k3_time_budget_ms'] *= 0.8
            self.parameters['k4_time_budget_ms'] *= 0.7
            self.parameters['approximation_accuracy'] = max(0.7, self.parameters['approximation_accuracy'] * 0.9)
            
        elif roi_ratio > 1.2:  # ROI muy alto
            # Podemos permitir más cómputo para mejor calidad
            self.parameters['k3_time_budget_ms'] = min