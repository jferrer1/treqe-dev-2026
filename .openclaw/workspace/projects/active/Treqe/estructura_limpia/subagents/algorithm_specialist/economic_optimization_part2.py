#!/usr/bin/env python3
"""
PARTE 2: Sistema de optimización económica completa
"""

import time
import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass
from economic_optimization import EconomicUser, EconomicDecisionSystem, AdaptiveOptimizer
import json

# ========== SIMULADOR DE MERCADO REAL ==========

class MarketSimulator:
    """Simula condiciones reales de mercado Treqe"""
    
    def __init__(self, n_users=100):
        self.n_users = n_users
        self.users = self.create_realistic_users(n_users)
        self.decision_system = EconomicDecisionSystem()
        self.optimizer = AdaptiveOptimizer()
        
    def create_realistic_users(self, n_users):
        """Crea usuarios con distribución realista de Treqe"""
        users = []
        
        # Distribuciones realistas basadas en data de marketplace
        reputation_dist = np.random.beta(2, 5, n_users) * 1000  # Sesgado hacia bajas reputaciones
        n_items_dist = np.random.poisson(2.5, n_users) + 1     # 1-6 items por usuario
        
        for i in range(n_users):
            n_offered = min(int(n_items_dist[i]), 6)
            n_desired = min(int(np.random.poisson(3) + 1), 8)
            
            # Valores realistas: mayoría items €50-€300, algunos caros
            if np.random.random() < 0.8:  # 80% items normales
                offered_values = np.random.uniform(50, 300, n_offered)
                desired_values = np.random.uniform(50, 400, n_desired)
            else:  # 20% items caros
                offered_values = np.random.uniform(200, 1000, n_offered)
                desired_values = np.random.uniform(200, 1500, n_desired)
            
            users.append(EconomicUser(
                id=i,
                reputation=float(reputation_dist[i]),
                offered_values=offered_values,
                desired_values=desired_values,
                offered_ids=np.arange(i*10, i*10 + n_offered),
                desired_ids=np.random.randint(0, n_users*10, n_desired)
            ))
        
        return users
    
    def build_compatibility_matrix(self):
        """Construye matriz de compatibilidad realista"""
        n = len(self.users)
        compatibility = np.zeros((n, n), dtype=bool)
        
        # Reglas realistas de compatibilidad:
        # 1. Usuarios con reputación similar tienden a ser compatibles
        # 2. Items de valor similar son más compatibles
        # 3. Densidad de ~20-30% (marketplace real)
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                    
                # Probabilidad base basada en diferencia de reputación
                rep_diff = abs(self.users[i].reputation - self.users[j].reputation) / 1000
                base_prob = 0.3 * (1.0 - rep_diff * 0.5)
                
                # Ajustar por valores de items
                avg_value_i = np.mean(self.users[i].offered_values)
                avg_value_j = np.mean(self.users[j].offered_values)
                value_ratio = min(avg_value_i, avg_value_j) / max(avg_value_i, avg_value_j)
                value_factor = 0.5 + value_ratio * 0.5
                
                # Probabilidad final
                prob = base_prob * value_factor
                
                if np.random.random() < prob:
                    compatibility[i, j] = True
        
        return compatibility
    
    def simulate_trading_round(self):
        """Simula una ronda de trading con decisiones económicas"""
        print("\n" + "="*70)
        print("SIMULACIÓN DE RONDA DE TRADING TREQE")
        print("="*70)
        
        # Condiciones actuales de mercado
        market_conditions = {
            'time_of_day': np.random.choice(['morning', 'afternoon', 'evening']),
            'day_of_week': np.random.choice(['weekday', 'weekend']),
            'user_activity': np.random.uniform(0.3, 0.8),  # 30-80% usuarios activos
            'avg_item_value': np.mean([np.mean(u.offered_values) for u in self.users])
        }
        
        print(f"\nCondiciones de mercado:")
        print(f"  Hora: {market_conditions['time_of_day']}")
        print(f"  Día: {market_conditions['day_of_week']}")
        print(f"  Actividad: {market_conditions['user_activity']*100:.1f}%")
        print(f"  Valor promedio item: €{market_conditions['avg_item_value']:.0f}")
        
        # Recomendación del sistema de decisión
        recommendations = self.decision_system.recommend_wheel_size(
            self.users, market_conditions
        )
        
        print(f"\nRECOMENDACIONES DEL SISTEMA ECONÓMICO:")
        for rec in recommendations:
            decision_symbol = "✅" if rec['decision'] in ['STRONG_RECOMMEND', 'RECOMMEND'] else "⚠️"
            print(f"\n  {decision_symbol} k={rec['k']}:")
            print(f"     ROI: {rec['roi']:.1f}x (objetivo: {self.decision_system.min_roi}x)")
            print(f"     Valor por usuario: €{rec['value_per_user']:.0f}")
            print(f"     Tiempo cómputo: {rec['computation_time']:.2f}s")
            print(f"     Decisión: {rec['decision']}")
        
        # Ejecutar matching con tamaño recomendado
        if recommendations:
            best_k = recommendations[0]['k']
            print(f"\nEJECUTANDO MATCHING con k={best_k}...")
            
            if best_k == 3:
                results = self.run_k3_matching()
            else:
                results = self.run_k4_matching_approximate()
            
            # Calcular métricas económicas reales
            economic_metrics = self.calculate_economic_metrics(results, best_k)
            
            print(f"\nRESULTADOS ECONÓMICOS:")
            print(f"  Valor total intercambiado: €{economic_metrics['total_value']:.0f}")
            print(f"  Coste computacional: €{economic_metrics['computation_cost']:.4f}")
            print(f"  ROI real: {economic_metrics['roi']:.1f}x")
            print(f"  Usuarios satisfechos: {economic_metrics['satisfied_users']}/{self.n_users}")
            print(f"  Valor por ciclo CPU: €{economic_metrics['value_per_cpu_cycle']:.2f}")
            
            # Ajustar optimizador basado en resultados
            self.optimizer.update_parameters(
                economic_metrics['roi'],
                self.decision_system.min_roi
            )
            
            return economic_metrics
        
        return None
    
    def run_k3_matching(self):
        """Ejecuta matching k=3 optimizado"""
        start_time = time.time()
        
        # Construir matriz de compatibilidad
        compatibility = self.build_compatibility_matrix()
        
        # Preparar datos para numba
        n_users = len(self.users)
        offered_values = np.array([u.offered_values.mean() for u in self.users])
        desired_values = np.array([u.desired_values.mean() for u in self.users])
        reputations = np.array([u.reputation for u in self.users])
        
        # Usar algoritmo optimizado
        from economic_optimization import find_profitable_k3_cycles_numba
        cycles, profits = find_profitable_k3_cycles_numba(
            n_users, compatibility, offered_values, desired_values,
            reputations, min_profit_per_cycle=10.0
        )
        
        elapsed = time.time() - start_time
        
        return {
            'cycles': cycles,
            'profits': profits,
            'computation_time': elapsed,
            'k': 3
        }
    
    def run_k4_matching_approximate(self):
        """Ejecuta matching k=4 aproximado (alto ROI)"""
        start_time = time.time()
        
        compatibility = self.build_compatibility_matrix()
        n_users = len(self.users)
        values = np.array([u.offered_values.mean() for u in self.users])
        reputations = np.array([u.reputation for u in self.users])
        
        from economic_optimization import find_high_roi_k4_approximate
        cycles, cycle_values = find_high_roi_k4_approximate(
            n_users, compatibility, values, reputations,
            time_budget_ms=5000  # 5 segundos máximo
        )
        
        elapsed = time.time() - start_time
        
        return {
            'cycles': cycles,
            'cycle_values': cycle_values,
            'computation_time': elapsed,
            'k': 4
        }
    
    def calculate_economic_metrics(self, results, k):
        """Calcula métricas económicas de los resultados"""
        total_value = 0
        satisfied_users = set()
        
        if k == 3:
            cycles = results['cycles']
            profits = results['profits']
            total_value = profits.sum() * 3  # Aproximación
            for cycle in cycles:
                satisfied_users.update(cycle)
        else:  # k == 4
            cycle_values = results['cycle_values']
            cycles = results['cycles']
            total_value = cycle_values.sum()
            for cycle in cycles:
                satisfied_users.update(cycle)
        
        # Costes
        computation_cost = results['computation_time'] * COST_CPU_PER_SECOND
        transaction_costs = total_value * 0.01  # 1% costes de transacción
        total_cost = computation_cost + transaction_costs
        
        # ROI
        roi = total_value / total_cost if total_cost > 0 else 0
        
        # Valor por ciclo CPU (métrica de eficiencia)
        cpu_cycles_approx = results['computation_time'] * 3.5e9  # 3.5 GHz CPU
        value_per_cpu_cycle = total_value / cpu_cycles_approx if cpu_cycles_approx > 0 else 0
        
        return {
            'total_value': total_value,
            'computation_cost': computation_cost,
            'transaction_costs': transaction_costs,
            'total_cost': total_cost,
            'roi': roi,
            'satisfied_users': len(satisfied_users),
            'value_per_cpu_cycle': value_per_cpu_cycle,
            'computation_time': results['computation_time']
        }

# ========== ANÁLISIS DE SENSIBILIDAD ECONÓMICA ==========

def economic_sensitivity_analysis():
    """Analiza sensibilidad del ROI a diferentes parámetros"""
    print("\n" + "="*70)
    print("ANÁLISIS DE SENSIBILIDAD ECONÓMICA")
    print("="*70)
    
    # Parámetros a variar
    param_ranges = {
        'n_users': [50, 100, 150, 200],
        'avg_item_value': [100, 250, 500, 1000],
        'market_density': [0.1, 0.2, 0.3, 0.4],
        'computation_cost_per_sec': [0.000001, 0.00001, 0.0001]
    }
    
    results = []
    
    for n_users in param_ranges['n_users']:
        print(f"\n--- {n_users} usuarios ---")
        
        simulator = MarketSimulator(n_users=n_users)
        
        # Variar valor promedio
        for avg_val in [100, 500]:
            # Ajustar valores de items
            for user in simulator.users:
                user.offered_values = np.random.uniform(avg_val*0.5, avg_val*1.5, len(user.offered_values))
                user.desired_values = np.random.uniform(avg_val*0.5, avg_val*1.5, len(user.desired_values))
            
            # Simular
            metrics = simulator.simulate_trading_round()
            
            if metrics:
                results.append({
                    'n_users': n_users,
                    'avg_item_value': avg_val,
                    'roi': metrics['roi'],
                    'value_per_cpu_cycle': metrics['value_per_cpu_cycle'],
                    'computation_time': metrics['computation_time']
                })
    
    # Análisis de resultados
    print("\n" + "="*70)
    print("CONCLUSIONES DEL ANÁLISIS DE SENSIBILIDAD")
    print("="*70)
    
    # Agrupar por número de usuarios
    from collections import defaultdict
    grouped = defaultdict(list)
    
    for r in results:
        grouped[r['n_users']].append(r)
    
    for n_users, group_results in sorted(grouped.items()):
        avg_roi = np.mean([r['roi'] for r in group_results])
        avg_value_per_cycle = np.mean([r['value_per_cpu_cycle'] for r in group_results])
        
        print(f"\n{n_users} usuarios:")
        print(f"  ROI promedio: {avg_roi:.1f}x")
        print(f"  Valor por ciclo CPU: €{avg_value_per_cycle:.4f}")
        
        # Determinar viabilidad económica
        if avg_roi >= 2.0:
            print(f"  ✅ VIABLE ECONÓMICAMENTE (ROI ≥ 2x)")
        elif avg_roi >= 1.0:
            print(f"  ⚠️  MARGINAL (1x ≤ ROI < 2x)")
        else:
            print(f"  ❌ NO VIABLE (ROI < 1x)")
    
    return results

# ========== RECOMENDACIONES DE OPTIMIZACIÓN ==========

def generate_optimization_recommendations():
    """Genera recomendaciones concretas de optimización"""
    print("\n" + "="*70)
    print("RECOMENDACIONES DE OPTIMIZACIÓN ECONÓMICA")
    print("="*70)
    
    recommendations = [
        {
            'priority': 1,
            'area': 'Algoritmo k=3',
            'action': 'Implementar numba + paralelización',
            'expected_improvement': '10-50x más rápido',
            'roi_impact': 'ROI +50-200%',
            'effort': '2-3 días',
            'economic_justification': 'k=3 tiene mejor valor/usuario, optimizarlo maximiza ROI'
        },
        {
            'priority': 2,
            'area': 'Matriz de compatibilidad',
            'action': 'Usar sparse matrices + caching',
            'expected_improvement': '5-20x menos memoria, 2-10x más rápido',
            'roi_impact': 'ROI +20-50%',
            'effort': '1-2 días',
            'economic_justification': 'Reduce coste computacional base'
        },
        {
            'priority': 3,
            'area': 'k=4 aproximado',
            'action': 'Algoritmo greedy con time budget',
            'expected_improvement': '100-1000x más rápido que exacto',
            'roi_impact': 'Hace k=4 económicamente viable (ROI > 1.5x)',
            'effort': '3-5 días',
            'economic_justification': 'Permite ofrecer k=4 como opción premium sin destruir ROI'
        },
        {
            'priority': 4,
            'area': 'Sistema de decisión',
            'action': 'Adaptive optimizer basado en ROI',
            'expected_improvement': 'ROI consistentemente > 2x',
            'roi_impact': '+30-100% ROI en condiciones variables',
            'effort': '2-4 días',
            'economic_justification': 'Maximiza ROI bajo diferentes condiciones de mercado'
        },
        {
            'priority': 5,
            'area': 'GPU acceleration',
            'action': 'Portar operaciones críticas a CUDA',
            'expected_improvement': '50-200x más rápido para operaciones masivas',
            'roi_impact': 'ROI +100-500% para grandes volúmenes',
            'effort': '1-2 semanas',
            'economic_justification': 'Escalabilidad económica para >1000 usuarios'
        }
    ]
    
    # Ordenar por prioridad
    recommendations.sort(key=lambda x: x['priority'])
    
    for rec in recommendations:
        print(f"\n{rec['priority']}. {rec['area']}:")
        print(f"   Acción: {rec['action']}")
        print(f"   Mejora esperada: {rec['expected_improvement']}")
        print(f"   Impacto ROI: {rec['roi_impact']}")
        print(f"   Esfuerzo: {rec['effort']}")
        print(f"   Justificación económica: {rec['economic_justification']}")
    
    # ROI esperado total
    print(f"\n{'='*70}")
    print("IMPACTO ECONÓMICO TOTAL ESPERADO:")
    print("="*70)
    
    base_roi = 1.5  # ROI base estimado
    cumulative_impact = 1.0
    
    for rec in recommendations:
        # Extraer % de mejora del string
        impact_str = rec['roi_impact']
        if '+' in impact_str and '%' in impact_str:
            percent = float(impact_str.split('+')[1].split('%')[0]) / 100
            cumulative_impact *= (1 + percent)
    
    expected_roi = base_roi * cumulative_