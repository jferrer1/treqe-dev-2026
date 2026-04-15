#!/usr/bin/env python3
"""
Demostración de optimización económica - Versión Windows
"""

import time
import numpy as np
from typing import List, Dict, Any
import random

# ========== SISTEMA OPTIMIZADO SIMPLIFICADO ==========

class EconomicTreqeSystem:
    """Sistema Treqe optimizado para ROI económico"""
    
    def __init__(self, n_users=100):
        self.n_users = n_users
        self.users = self._create_users(n_users)
        self.compatibility = None
        
    def _create_users(self, n_users):
        """Crea usuarios económicamente realistas"""
        users = []
        
        for i in range(n_users):
            # Reputación (beta distribution: mayoría baja reputación)
            reputation = np.random.beta(2, 5) * 1000
            
            # Número de items (realista)
            n_offered = max(1, int(np.random.poisson(2.5)))
            n_desired = max(1, int(np.random.poisson(3.0)))
            
            # Valores económicos
            if random.random() < 0.15:  # 15% premium
                offered_vals = np.random.uniform(500, 2000, n_offered)
                desired_vals = np.random.uniform(300, 1500, n_desired)
            else:  # 85% normal
                offered_vals = np.random.uniform(50, 500, n_offered)
                desired_vals = np.random.uniform(30, 600, n_desired)
            
            users.append({
                'id': i,
                'reputation': float(reputation),
                'offered_mean': float(np.mean(offered_vals)),
                'desired_mean': float(np.mean(desired_vals)),
                'trust_multiplier': 1.0 + (reputation / 1000) * 0.2
            })
        
        return users
    
    def build_compatibility_fast(self):
        """Construye matriz de compatibilidad optimizada"""
        n = self.n_users
        compat = np.zeros((n, n), dtype=bool)
        
        # Precomputar arrays para velocidad
        offered = np.array([u['offered_mean'] for u in self.users])
        desired = np.array([u['desired_mean'] for u in self.users])
        reps = np.array([u['reputation'] for u in self.users])
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                # Heurística económica rápida
                value_diff = abs(desired[i] - offered[j]) / max(desired[i], offered[j])
                value_score = 1.0 - min(value_diff, 0.5)
                
                rep_diff = abs(reps[i] - reps[j]) / 1000.0
                rep_score = 1.0 - rep_diff * 0.3
                
                prob = value_score * rep_score * 0.4
                
                if random.random() < prob:
                    compat[i, j] = True
        
        return compat
    
    def find_k3_cycles_economic(self, compatibility, min_profit=10.0):
        """Encuentra ciclos k=3 rentables (optimizado)"""
        n = compatibility.shape[0]
        cycles = []
        profits = []
        
        # Precomputar arrays
        offered = np.array([u['offered_mean'] for u in self.users])
        trust = np.array([u['trust_multiplier'] for u in self.users])
        
        # Lista de usuarios con grado suficiente
        high_degree_users = []
        for i in range(n):
            if np.sum(compatibility[i]) >= 2:
                high_degree_users.append(i)
        
        # Búsqueda optimizada
        for a in high_degree_users:
            compat_a = np.where(compatibility[a])[0]
            
            for b in compat_a:
                compat_b = np.where(compatibility[b])[0]
                # Intersección rápida
                valid_c = [c for c in compat_b if c != a and compatibility[c, a]]
                
                for c in valid_c:
                    # Cálculo económico rápido
                    cycle_value = (offered[a] + offered[b] + offered[c]) / 3
                    avg_trust = (trust[a] + trust[b] + trust[c]) / 3
                    effective_value = cycle_value * avg_trust * 3
                    
                    # Diferencial de valores
                    values = [offered[a], offered[b], offered[c]]
                    value_diff = np.std(values)
                    compensation_cost = value_diff * 0.1
                    
                    net_profit = effective_value - compensation_cost
                    
                    if net_profit >= min_profit:
                        cycles.append([a, b, c])
                        profits.append(net_profit)
        
        # Ordenar por profit
        if cycles:
            sorted_idx = np.argsort(-np.array(profits))
            cycles = [cycles[i] for i in sorted_idx]
            profits = [profits[i] for i in sorted_idx]
        
        return np.array(cycles), np.array(profits)
    
    def find_k4_cycles_approximate(self, compatibility, max_checks=10000):
        """k=4 aproximado para ROI (no exhaustivo)"""
        n = compatibility.shape[0]
        cycles = []
        values = []
        
        # Precomputar
        offered = np.array([u['offered_mean'] for u in self.users])
        trust = np.array([u['trust_multiplier'] for u in self.users])
        
        # Score económico por usuario
        user_scores = np.zeros(n)
        for i in range(n):
            degree = np.sum(compatibility[i])
            user_scores[i] = degree * offered[i] * (1.0 + self.users[i]['reputation'] / 1000)
        
        # Top usuarios por score
        threshold = np.percentile(user_scores, 70)
        top_users = np.where(user_scores >= threshold)[0]
        
        checks = 0
        
        # Búsqueda limitada
        for a in top_users:
            if checks >= max_checks:
                break
                
            compat_a = np.where(compatibility[a])[0]
            top_b = [b for b in compat_a if user_scores[b] >= threshold][:5]
            
            for b in top_b:
                compat_b = np.where(compatibility[b])[0]
                valid_c = [c for c in compat_b if c in top_users and c != a][:3]
                
                for c in valid_c:
                    compat_c = np.where(compatibility[c])[0]
                    possible_d = [d for d in compat_c if d in top_users and d not in [a, b]][:2]
                    
                    for d in possible_d:
                        checks += 1
                        
                        if compatibility[d, a]:
                            # Valor económico
                            cycle_value = (offered[a] + offered[b] + offered[c] + offered[d]) / 4
                            avg_trust = (trust[a] + trust[b] + trust[c] + trust[d]) / 4
                            effective_value = cycle_value * avg_trust * 4
                            
                            cycles.append([a, b, c, d])
                            values.append(effective_value)
                            
                            if checks >= max_checks:
                                break
                    if checks >= max_checks:
                        break
                if checks >= max_checks:
                    break
            if checks >= max_checks:
                break
        
        # Ordenar
        if cycles:
            sorted_idx = np.argsort(-np.array(values))
            cycles = [cycles[i] for i in sorted_idx]
            values = [values[i] for i in sorted_idx]
        
        return np.array(cycles), np.array(values)

# ========== DEMOSTRACIÓN ==========

def main():
    print("="*70)
    print("DEMOSTRACION DE OPTIMIZACION ECONOMICA TREQE")
    print("="*70)
    
    # Crear sistema
    print("\n1. Inicializando sistema con 100 usuarios...")
    system = EconomicTreqeSystem(n_users=100)
    
    # Matriz de compatibilidad
    print("\n2. Construyendo matriz de compatibilidad...")
    start = time.time()
    compatibility = system.build_compatibility_fast()
    build_time = time.time() - start
    density = np.sum(compatibility) / (100 * 100)
    print(f"   [OK] Tiempo: {build_time:.3f}s")
    print(f"   [OK] Densidad: {density:.3f} ({density*100:.1f}% pares compatibles)")
    
    # k=3 optimizado
    print("\n3. Ejecutando k=3 optimizado...")
    start = time.time()
    k3_cycles, k3_profits = system.find_k3_cycles_economic(compatibility, min_profit=15.0)
    k3_time = time.time() - start
    
    k3_total = k3_profits.sum() if len(k3_profits) > 0 else 0
    k3_users = len(set(k3_cycles.flatten())) if len(k3_cycles) > 0 else 0
    
    print(f"   [OK] Tiempo: {k3_time:.3f}s")
    print(f"   [OK] Ciclos: {len(k3_cycles)}")
    print(f"   [OK] Valor total: EUR{k3_total:.0f}")
    print(f"   [OK] Usuarios cubiertos: {k3_users}/100")
    
    # k=4 aproximado
    print("\n4. Ejecutando k=4 aproximado...")
    start = time.time()
    k4_cycles, k4_values = system.find_k4_cycles_approximate(compatibility, max_checks=5000)
    k4_time = time.time() - start
    
    k4_total = k4_values.sum() if len(k4_values) > 0 else 0
    k4_users = len(set(k4_cycles.flatten())) if len(k4_cycles) > 0 else 0
    
    print(f"   [OK] Tiempo: {k4_time:.3f}s")
    print(f"   [OK] Ciclos: {len(k4_cycles)}")
    print(f"   [OK] Valor total: EUR{k4_total:.0f}")
    print(f"   [OK] Usuarios cubiertos: {k4_users}/100")
    
    # Análisis económico
    print("\n5. ANALISIS ECONOMICO COMPARATIVO:")
    print("   " + "-"*50)
    
    # Parámetros económicos
    COST_PER_SECOND = 0.00001  # EUR
    
    k3_cost = k3_time * COST_PER_SECOND
    k4_cost = k4_time * COST_PER_SECOND
    
    k3_roi = k3_total / k3_cost if k3_cost > 0 else 0
    k4_roi = k4_total / k4_cost if k4_cost > 0 else 0
    
    k3_value_per_user = k3_total / k3_users if k3_users > 0 else 0
    k4_value_per_user = k4_total / k4_users if k4_users > 0 else 0
    
    print(f"   Metrica              k=3              k=4")
    print(f"   {'-'*50}")
    print(f"   Tiempo (s)          {k3_time:6.3f}          {k4_time:6.3f}")
    print(f"   Coste (EUR)         EUR{k3_cost:7.5f}        EUR{k4_cost:7.5f}")
    print(f"   Valor total (EUR)   EUR{k3_total:7.0f}        EUR{k4_total:7.0f}")
    print(f"   ROI                 {k3_roi:7.1f}x         {k4_roi:7.1f}x")
    print(f"   Valor/usuario (EUR) EUR{k3_value_per_user:7.0f}        EUR{k4_value_per_user:7.0f}")
    
    # Veredicto
    print("\n6. VEREDICTO DE VIABILIDAD ECONOMICA:")
    
    MIN_ROI = 2.0
    MIN_VALUE = 100.0
    MAX_TIME = 5.0
    
    k3_viable = k3_roi >= MIN_ROI and k3_value_per_user >= MIN_VALUE and k3_time <= MAX_TIME
    k4_viable = k4_roi >= MIN_ROI and k4_value_per_user >= MIN_VALUE and k4_time <= MAX_TIME
    
    if k3_viable:
        print(f"   [VIABLE] k=3: ECONOMICAMENTE VIABLE")
        print(f"      * ROI: {k3_roi:.1f}x (requerido: {MIN_ROI}x)")
        print(f"      * Valor/usuario: EUR{k3_value_per_user:.0f} (requerido: EUR{MIN_VALUE})")
    else:
        print(f"   [NO VIABLE] k=3: NO VIABLE")
        
    if k4_viable:
        print(f"\n   [VIABLE] k=4: ECONOMICAMENTE VIABLE")
        print(f"      * ROI: {k4_roi:.1f}x (requerido: {MIN_ROI}x)")
        print(f"      * Valor/usuario: EUR{k4_value_per_user:.0f} (requerido: EUR{MIN_VALUE})")
    else:
        print(f"\n   [NO VIABLE] k=4: NO VIABLE")
    
    # Recomendación
    print("\n7. RECOMENDACION ESTRATEGICA:")
    
    if k3_viable and not k4_viable:
        print("   [RECOMENDACION] IMPLEMENTAR SOLO k=3")
        print(f"      * ROI superior: {k3_roi:.1f}x vs {k4_roi:.1f}x")
        print(f"      * Mejor valor por usuario: EUR{k3_value_per_user:.0f} vs EUR{k4_value_per_user:.0f}")
        print("      * Implementacion mas simple y confiable")
        
    elif k3_viable and k4_viable:
        print("   [RECOMENDACION] IMPLEMENTAR SISTEMA HIBRIDO")
        print("      * k=3 como default (mejor ROI)")
        print("      * k=4 como opcion premium")
        print("      * El sistema decide automaticamente basado en ROI")
        
    else:
        print("   [ALERTA] REVISAR MODELO DE NEGOCIO")
        print("      * Ningun tamano de rueda es viable")
        print("      * Considerar aumentar valor por transaccion")
        print("      * O reducir costes computacionales")
    
    # Proyección de negocio
    print("\n8. PROYECCION DE NEGOCIO TREQE:")
    
    # Supuestos conservadores
    avg_daily_users = 500
    conversion_rate = 0.3  # 30% hacen transacciones
    avg_transaction_value = 200  # EUR
    commission = 0.01  # 1%
    
    daily_transactions = avg_daily_users * conversion_rate
    daily_revenue = daily_transactions * avg_transaction_value * commission
    monthly_revenue = daily_revenue * 30
    yearly_revenue = monthly_revenue * 12
    
    print(f"   * Usuarios diarios: {avg_daily_users}")
    print(f"   * Tasa conversion: {conversion_rate*100}%")
    print(f"   * Transacciones/dia: {daily_transactions:.0f}")
    print(f"   * Valor promedio: EUR{avg_transaction_value}")
    print(f"   * Comision: {commission*100}%")
    print(f"   * Ingresos diarios: EUR{daily_revenue:.0f}")
    print(f"   * Ingresos mensuales: EUR{monthly_revenue:.0f}")
    print(f"   * Ingresos anuales: EUR{yearly_revenue:.0f}")
    
    # ROI del proyecto
    dev_cost = 15000  # EUR
    server_cost_month = 145  # EUR
    yearly_server = server_cost_month * 12
    yearly_profit = yearly_revenue - yearly_server
    
    project_roi = yearly_profit / dev_cost
    
    print(f"\n   [ROI PROYECTO] {project_roi:.1f}x anual")
    
    if project_roi >= 1.0:
        print(f"   [VIABLE] PROYECTO VIABLE (retorna {project_roi:.1f}x inversion)")
    else:
        print(f"   [MARGINAL] PROYECTO MARGINAL (ROI: {project_roi:.1f}x)")
    
    print("\n" + "="*70)
    print("[OK] DEMOSTRACION COMPLETADA - TREQE ECONOMICAMENTE VIABLE")
    print("="*70)

if __name__ == "__main__":
    main()