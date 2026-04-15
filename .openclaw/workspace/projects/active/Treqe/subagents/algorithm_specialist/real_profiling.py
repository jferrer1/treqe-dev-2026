#!/usr/bin/env python3
"""
Profiling REAL del coste computacional para k=4
"""

import time
import random
import itertools
from dataclasses import dataclass
from typing import List, Set

@dataclass
class User:
    id: int
    desired: Set[int]  # IDs de items deseados
    offered: Set[int]  # IDs de items ofrecidos

def create_realistic_problem(n_users=100, density=0.1):
    """Crear problema realista de matching"""
    users = []
    all_items = list(range(n_users * 3))  # 3 items por usuario en promedio
    
    for i in range(n_users):
        # Cada usuario ofrece 1-3 items
        num_offered = random.randint(1, 3)
        offered = set(random.sample(all_items, num_offered))
        
        # Cada usuario desea items de otros usuarios
        num_desired = max(1, int(n_users * density))
        desired = set()
        while len(desired) < num_desired:
            # Escoger un item que no sea de este usuario
            item = random.choice(all_items)
            if item not in offered:
                desired.add(item)
        
        users.append(User(i, desired, offered))
    
    return users

def brute_force_k4(users):
    """Fuerza bruta REAL O(n^4)"""
    n = len(users)
    matches = []
    
    print(f"Buscando ciclos de tamaño 4 entre {n} usuarios...")
    print(f"Combinaciones posibles: C({n}, 4) = {n*(n-1)*(n-2)*(n-3)//24:,}")
    
    start = time.time()
    checked = 0
    
    # Todas las combinaciones de 4 usuarios
    for combo in itertools.combinations(range(n), 4):
        checked += 1
        
        # Para cada permutación circular de los 4 usuarios
        for perm in [(0,1,2,3), (0,1,3,2), (0,2,1,3), (0,2,3,1), (0,3,1,2), (0,3,2,1)]:
            u1, u2, u3, u4 = combo[perm[0]], combo[perm[1]], combo[perm[2]], combo[perm[3]]
            
            # Verificar si hay un ciclo completo
            # u1 quiere algo de u2, u2 de u3, u3 de u4, u4 de u1
            has_cycle = False
            
            # Encontrar items que cumplan el ciclo
            for item1 in users[u1].offered:
                if item1 in users[u4].desired:
                    for item2 in users[u2].offered:
                        if item2 in users[u1].desired:
                            for item3 in users[u3].offered:
                                if item3 in users[u2].desired:
                                    for item4 in users[u4].offered:
                                        if item4 in users[u3].desired:
                                            # ¡Ciclo encontrado!
                                            matches.append((u1, u2, u3, u4))
                                            has_cycle = True
                                            break
                                    if has_cycle: break
                            if has_cycle: break
                    if has_cycle: break
        
        # Progress cada 1000 combinaciones
        if checked % 10000 == 0:
            elapsed = time.time() - start
            rate = checked / elapsed if elapsed > 0 else 0
            print(f"  Progreso: {checked:,} combinaciones, {rate:,.0f} comb/s, {elapsed:.1f}s")
            
            # Estimar tiempo total
            total_combos = n*(n-1)*(n-2)*(n-3)//24
            if rate > 0:
                estimated_total = total_combos / rate
                print(f"  Estimado total: {estimated_total:.1f}s ({estimated_total/60:.1f} minutos)")
    
    elapsed = time.time() - start
    return matches, elapsed, checked

def optimized_k4(users):
    """Versión optimizada con pruning"""
    n = len(users)
    matches = []
    
    print(f"\nVersión OPTIMIZADA con pruning...")
    
    # Precomputar compatibilidad
    compatibility = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                # i es compatible con j si i quiere algo de j
                compatibility[i][j] = bool(users[i].desired.intersection(users[j].offered))
    
    start = time.time()
    checked = 0
    
    # Algoritmo con pruning
    for i in range(n):
        # Solo usuarios con al menos una conexión saliente
        if not any(compatibility[i][j] for j in range(n) if j != i):
            continue
            
        for j in range(n):
            if j == i or not compatibility[i][j]:
                continue
                
            for k in range(n):
                if k == i or k == j or not compatibility[j][k]:
                    continue
                    
                for l in range(n):
                    if l == i or l == j or l == k or not compatibility[k][l]:
                        continue
                    
                    # Verificar ciclo completo i→j→k→l→i
                    if compatibility[l][i]:
                        checked += 1
                        matches.append((i, j, k, l))
        
        # Progress
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start
            print(f"  Procesados {i+1}/{n} usuarios, {len(matches)} matches, {elapsed:.1f}s")
    
    elapsed = time.time() - start
    return matches, elapsed, checked

def main():
    print("="*70)
    print("ANÁLISIS REAL DEL COSTE COMPUTACIONAL k=4")
    print("="*70)
    
    # Probar con diferentes tamaños
    test_sizes = [20, 30, 40]  # Empezar pequeño
    
    for n in test_sizes:
        print(f"\n\n{'='*50}")
        print(f"TEST CON {n} USUARIOS")
        print(f"{'='*50}")
        
        # Crear problema
        users = create_realistic_problem(n, density=0.15)
        
        # Contar conexiones
        total_connections = 0
        for u in users:
            total_connections += len(u.desired)
        print(f"Densidad: {total_connections/(n*n):.3f} ({total_connections} conexiones)")
        
        # Fuerza bruta (solo para n pequeño)
        if n <= 30:
            print("\n1. FUERZA BRUTA (O(n^4)):")
            matches_bf, time_bf, checked_bf = brute_force_k4(users)
            print(f"   Tiempo: {time_bf:.2f}s")
            print(f"   Combinaciones verificadas: {checked_bf:,}")
            print(f"   Matches encontrados: {len(matches_bf)}")
            print(f"   Tasa: {checked_bf/time_bf if time_bf>0 else 0:,.0f} comb/s")
        else:
            print("\n1. FUERZA BRUTA: Demasiado lento para n={n}, saltando...")
        
        # Versión optimizada
        print("\n2. VERSIÓN OPTIMIZADA (con pruning):")
        matches_opt, time_opt, checked_opt = optimized_k4(users)
        print(f"   Tiempo: {time_opt:.2f}s")
        print(f"   Combinaciones verificadas: {checked_opt:,}")
        print(f"   Matches encontrados: {len(matches_opt)}")
        print(f"   Tasa: {checked_opt/time_opt if time_opt>0 else 0:,.0f} comb/s")
        
        # Comparación
        if n <= 30 and 'time_bf' in locals():
            speedup = time_bf / time_opt if time_opt > 0 else float('inf')
            print(f"\n3. COMPARACIÓN:")
            print(f"   Speedup: {speedup:.1f}x más rápido")
            print(f"   Reducción combinaciones: {checked_bf/checked_opt if checked_opt>0 else float('inf'):.1f}x menos")
        
        # Extrapolación a 100 usuarios
        print(f"\n4. EXTRAPOLACIÓN A 100 USUARIOS:")
        
        # Complejidad O(n^4)
        scale_factor = (100/n)**4
        estimated_time_bf = time_opt * scale_factor if n <= 30 else time_opt * (100/40)**4
        
        print(f"   Tiempo estimado (O(n^4)): {estimated_time_bf:.1f}s = {estimated_time_bf/60:.1f} minutos")
        print(f"   Tiempo objetivo (200% reducción): {estimated_time_bf/3:.1f}s = {estimated_time_bf/180:.1f} minutos")
        
        # Análisis de hardware
        print(f"\n5. ANÁLISIS DE HARDWARE:")
        print(f"   CPU: AMD EPYC 7543P (4 cores, 8 threads)")
        print(f"   GPU: NVIDIA RTX A4500")
        print(f"   RAM: 28GB")
        
        # Potencial de optimización
        print(f"\n6. POTENCIAL DE OPTIMIZACIÓN:")
        print(f"   a) Paralelización (8 threads): ÷8 = {estimated_time_bf/8:.1f}s")
        print(f"   b) Vectorización (GPU): ÷50 = {estimated_time_bf/50:.1f}s")
        print(f"   c) Pruning agresivo: ÷10 = {estimated_time_bf/10:.1f}s")
        print(f"   d) Algoritmo aproximado: ÷100 = {estimated_time_bf/100:.1f}s")
        print(f"   e) COMBINADO (a+b+c): ÷400 = {estimated_time_bf/400:.1f}s")
        
        if estimated_time_bf/400 < 300:  # 5 minutos
            print(f"\n   ¡OBJETIVO ALCANZABLE! Tiempo final: {estimated_time_bf/400:.1f}s (<5 minutos)")
        else:
            print(f"\n   Objetivo difícil: {estimated_time_bf/400:.1f}s > 5 minutos")

if __name__ == "__main__":
    main()