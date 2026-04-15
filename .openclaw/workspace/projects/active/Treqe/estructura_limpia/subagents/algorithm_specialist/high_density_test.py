#!/usr/bin/env python3
"""
Test con ALTA DENSIDAD (como Treqe real)
"""

import time
import random
from dataclasses import dataclass
from typing import List, Set
import sys

@dataclass
class User:
    id: int
    desired: Set[int]
    offered: Set[int]

def create_high_density_problem(n_users=100, avg_desires=10, avg_offers=3):
    """Crear problema con ALTA densidad (como marketplace real)"""
    users = []
    all_items = list(range(n_users * avg_offers))
    
    # Primero, crear ofertas
    item_owners = {}
    item_idx = 0
    
    for user_id in range(n_users):
        num_offers = random.randint(avg_offers-1, avg_offers+1)
        offered = set()
        
        for _ in range(num_offers):
            if item_idx < len(all_items):
                item_id = all_items[item_idx]
                offered.add(item_id)
                item_owners[item_id] = user_id
                item_idx += 1
        
        users.append(User(user_id, set(), offered))
    
    # Ahora, crear deseos con ALTA densidad
    for user in users:
        # Cada usuario desea muchos items (marketplace real)
        num_desires = random.randint(avg_desires-3, avg_desires+3)
        
        for _ in range(num_desires):
            # Escoger un item aleatorio que NO sea del propio usuario
            while True:
                item_id = random.choice(all_items)
                owner = item_owners.get(item_id)
                if owner != user.id and item_id not in user.desired:
                    user.desired.add(item_id)
                    break
    
    return users, item_owners

def brute_force_k4_simple(users, timeout=10):
    """Fuerza bruta SIMPLE para entender complejidad real"""
    n = len(users)
    matches = 0
    operations = 0
    
    print(f"  Fuerza bruta k=4 (n={n})...")
    print(f"  Combinaciones teóricas: C({n},4) = {n*(n-1)*(n-2)*(n-3)//24:,}")
    
    start = time.time()
    
    # Versión SIMPLE para medir coste
    for a in range(min(n, 30)):  # Limitar para no explotar
        if time.time() - start > timeout:
            break
            
        for b in range(n):
            if b == a: continue
            operations += 1
            
            # Verificar si a quiere algo de b
            a_wants_b = False
            for item in users[b].offered:
                if item in users[a].desired:
                    a_wants_b = True
                    break
            
            if not a_wants_b:
                continue
                
            for c in range(n):
                if c in (a, b): continue
                operations += 1
                
                # b quiere algo de c?
                b_wants_c = False
                for item in users[c].offered:
                    if item in users[b].desired:
                        b_wants_c = True
                        break
                
                if not b_wants_c:
                    continue
                    
                for d in range(n):
                    if d in (a, b, c): continue
                    operations += 1
                    
                    # c quiere algo de d?
                    c_wants_d = False
                    for item in users[d].offered:
                        if item in users[c].desired:
                            c_wants_d = True
                            break
                    
                    if not c_wants_d:
                        continue
                    
                    # d quiere algo de a?
                    d_wants_a = False
                    for item in users[a].offered:
                        if item in users[d].desired:
                            d_wants_a = True
                            break
                    
                    if d_wants_a:
                        matches += 1
    
    elapsed = time.time() - start
    return matches, elapsed, operations

def main():
    print("="*80)
    print("ANÁLISIS CON ALTA DENSIDAD (Treqe REAL)")
    print("="*80)
    
    # Configuración REALISTA de Treqe:
    # - Cada usuario ofrece 2-4 items
    # - Cada usuario desea 8-12 items (alta densidad)
    # - ~20-30% de pares de usuarios son compatibles
    
    test_cases = [
        (30, 3, 8, "Pequeño (30u)"),
        (50, 3, 10, "Mediano (50u)"),
        (70, 3, 10, "Grande (70u)"),
        (100, 3, 12, "Real (100u)")
    ]
    
    for n_users, avg_offers, avg_desires, desc in test_cases:
        print(f"\n{'='*60}")
        print(f"{desc}: {n_users} usuarios, {avg_offers} ofertas/u, {avg_desires} deseos/u")
        print(f"{'='*60}")
        
        # Crear problema
        users, item_owners = create_high_density_problem(n_users, avg_desires, avg_offers)
        
        # Calcular densidad REAL
        total_possible_pairs = n_users * (n_users - 1)
        compatible_pairs = 0
        
        for i in range(n_users):
            for j in range(n_users):
                if i != j:
                    # i quiere algo de j?
                    if users[i].desired.intersection(users[j].offered):
                        compatible_pairs += 1
        
        density = compatible_pairs / total_possible_pairs
        
        print(f"Densidad real: {density:.3f} ({compatible_pairs}/{total_possible_pairs} pares compatibles)")
        print(f"Porcentaje: {density*100:.1f}%")
        
        # Estimar complejidad
        print(f"\nEstimación teórica O(n^4):")
        print(f"  n = {n_users}")
        print(f"  n^4 = {n_users**4:,}")
        print(f"  Operaciones estimadas: ~{n_users**4 * density**4:,.0f}")
        
        # Ejecutar fuerza bruta limitada
        print(f"\nEjecutando fuerza bruta (limitada a 10s)...")
        matches, elapsed, ops = brute_force_k4_simple(users, timeout=10)
        
        print(f"  Tiempo: {elapsed:.2f}s")
        print(f"  Operaciones: {ops:,}")
        print(f"  Matches: {matches}")
        
        if elapsed > 0:
            ops_per_sec = ops / elapsed
            print(f"  Operaciones/segundo: {ops_per_sec:,.0f}")
            
            # Extrapolar a búsqueda completa
            # Operaciones totales estimadas ≈ n^4 * density^3 (simplificado)
            estimated_total_ops = (n_users ** 4) * (density ** 3)
            estimated_total_time = estimated_total_ops / ops_per_sec if ops_per_sec > 0 else float('inf')
            
            print(f"\n  EXTRAPOLACIÓN a búsqueda COMPLETA:")
            print(f"  Operaciones totales estimadas: {estimated_total_ops:,.0f}")
            print(f"  Tiempo total estimado: {estimated_total_time:.1f}s = {estimated_total_time/60:.1f} minutos")
            
            # Para 100 usuarios
            if n_users == 100:
                print(f"\n  {'*'*50}")
                print(f"  CONCLUSIÓN PARA 100 USUARIOS:")
                print(f"  Tiempo estimado k=4: {estimated_total_time/60:.1f} minutos")
                
                # Objetivo: reducir 200% (3x más rápido)
                target_time = estimated_total_time / 3
                print(f"  Objetivo (200% reducción): {target_time/60:.1f} minutos")
                
                # ¿Es posible?
                if estimated_total_time > 300:  # > 5 minutos
                    print(f"  PROBLEMA: {estimated_total_time/60:.1f} minutos > 5 minutos límite")
                    print(f"  NECESITAMOS: {estimated_total_time/target_time:.1f}x más rápido")
                else:
                    print(f"  VIABLE: {estimated_total_time/60:.1f} minutos < 5 minutos")
    
    print(f"\n{'='*80}")
    print("ANÁLISIS DE OPTIMIZACIÓN NECESARIA")
    print("="*80)
    
    # Para 100 usuarios con densidad 0.2 (20% pares compatibles)
    n = 100
    density = 0.2
    
    # Operaciones teóricas
    ops_theoretical = n**4 * density**3
    print(f"\nPara n=100, densidad={density}:")
    print(f"  Operaciones teóricas: {ops_theoretical:,.0f}")
    
    # Hardware actual
    print(f"\nHardware disponible:")
    print(f"  CPU: AMD EPYC 7543P (4 cores, 8 threads)")
    print(f"  GPU: NVIDIA RTX A4500 (20 TFLOPS)")
    print(f"  RAM: 28GB")
    
    # Performance estimada
    cpu_ops_per_sec = 10_000_000  # 10M ops/sec (Python puro)
    gpu_ops_per_sec = 1_000_000_000  # 1B ops/sec (GPU optimizado)
    
    print(f"\nPerformance estimada:")
    print(f"  CPU (Python): {cpu_ops_per_sec:,.0f} ops/sec")
    print(f"  GPU (CUDA): {gpu_ops_per_sec:,.0f} ops/sec")
    
    # Tiempos estimados
    time_cpu = ops_theoretical / cpu_ops_per_sec
    time_gpu = ops_theoretical / gpu_ops_per_sec
    
    print(f"\nTiempos estimados:")
    print(f"  CPU only: {time_cpu:.1f}s = {time_cpu/60:.1f} minutos")
    print(f"  GPU optimized: {time_gpu:.1f}s = {time_gpu/60:.1f} minutos")
    
    # Optimizaciones adicionales
    print(f"\nOptimizaciones posibles:")
    
    optimizations = [
        ("Pruning (10x)", 10),
        ("Paralelización CPU (8x)", 8),
        ("Vectorización (4x)", 4),
        ("Algoritmo aproximado (100x)", 100),
        ("GPU acceleration (100x)", 100),
        ("Estructuras optimizadas (5x)", 5)
    ]
    
    current_speed = 1.0
    current_time = time_cpu
    
    for name, factor in optimizations:
        current_speed *= factor
        current_time /= factor
        print(f"  + {name}: ÷{factor} → {current_time:.1f}s ({current_time/60:.1f} minutos)")
        
        if current_time <= 300:  # 5 minutos
            print(f"    ¡OBJETIVO ALCANZADO con {name}!")
            break
    
    if current_time > 300:
        print(f"\n  ¡OBJETIVO DIFÍCIL! Necesitamos TODAS las optimizaciones:")
        total_speedup = 1.0
        for name, factor in optimizations:
            total_speedup *= factor
        final_time = time_cpu / total_speedup
        print(f"  Speedup total: {total_speedup:,.0f}x")
        print(f"  Tiempo final: {final_time:.1f}s = {final_time/60:.1f} minutos")
        
        if final_time <= 300:
            print(f"  ¡PERO POSIBLE! ({final_time/60:.1f} minutos)")
        else:
            print(f"  IMPOSIBLE ({final_time/60:.1f} minutos > 5 minutos)")
    
    print(f"\n{'='*80}")
    print("RECOMENDACIÓN FINAL:")
    print("="*80)
    print(f"1. k=4 con 100 usuarios y densidad realista (~20%) es COMPUTACIONALMENTE COSTOSO")
    print(f"2. Tiempo estimado: {time_cpu/60:.1f} minutos (CPU) → {time_gpu/60:.1f} minutos (GPU)")
    print(f"3. Para reducir 200% (3x más rápido), necesitamos GPU + algoritmos aproximados")
    print(f"4. El ROI económico de k=4 vs k=3 sigue siendo NEGATIVO (-€30/usuario)")
    print(f"5. RECOMENDACIÓN: Optimizar k=3 y considerar k=4 solo si:")
    print(f"   a) Los usuarios LO EXIGEN explícitamente")
    print(f"   b) Encontramos caso de uso específico donde k=4 da valor REAL")
    print(f"   c) Estamos dispuestos a invertir en GPU computing")
    print(f"   d) Aceptamos soluciones aproximadas (no óptimas)")

if __name__ == "__main__":
    main()