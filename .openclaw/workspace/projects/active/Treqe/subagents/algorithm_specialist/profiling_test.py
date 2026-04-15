#!/usr/bin/env python3
"""
Profiling del algoritmo actual para entender costes computacionales
"""

import time
import random
import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any

# ========== DATA STRUCTURES ==========

class UserLevel(Enum):
    NOVATO = 1
    MIEMBRO = 2
    CONFIABLE = 3
    ELITE = 4

@dataclass
class Item:
    id: str
    name: str
    value: float
    category: str

@dataclass 
class User:
    id: str
    name: str
    level: UserLevel
    reputation: float  # 0-1000
    offered_items: List[Item]
    desired_items: List[Item]
    
    def commission_rate(self) -> float:
        rates = {
            UserLevel.NOVATO: 0.01,
            UserLevel.MIEMBRO: 0.01,
            UserLevel.CONFIABLE: 0.009,
            UserLevel.ELITE: 0.008
        }
        return rates.get(self.level, 0.01)
    
    def reputation_multiplier(self) -> float:
        return 1.0 + (self.reputation / 1000) * 0.1

# ========== ALGORITMO ACTUAL (SIMPLIFICADO) ==========

def find_direct_matches_naive(users: List[User]) -> List[Dict]:
    """Algoritmo naive O(n^4) para k=2"""
    matches = []
    matched_users = set()
    matched_items = set()
    
    for i, user1 in enumerate(users):
        if user1.id in matched_users:
            continue
            
        for user2 in users[i+1:]:
            if user2.id in matched_users:
                continue
            
            for item1 in user1.offered_items:
                if item1.id in matched_items:
                    continue
                    
                for item2 in user2.offered_items:
                    if item2.id in matched_items:
                        continue
                    
                    # Direct match found
                    if (item1 in user2.desired_items and 
                        item2 in user1.desired_items):
                        
                        matches.append({
                            "participants": [user1.id, user2.id],
                            "items": [item1.id, item2.id]
                        })
                        matched_users.update([user1.id, user2.id])
                        matched_items.update([item1.id, item2.id])
                        break
                if user1.id in matched_users:
                    break
            if user1.id in matched_users:
                break
    
    return matches

def find_circular_matches_naive(users: List[User], k: int = 3) -> List[Dict]:
    """Algoritmo naive O(n^k) para k>2"""
    matches = []
    matched_users = set()
    matched_items = set()
    
    # Función recursiva para buscar ciclos
    def find_cycle(start_user, current_path, current_items, depth):
        if depth == k:
            # Verificar si el último usuario quiere el item del primero
            last_user = current_path[-1]
            first_item = current_items[0]
            if first_item in last_user.desired_items:
                return current_path, current_items
            return None, None
        
        current_user = current_path[-1] if current_path else start_user
        
        for next_user in users:
            if next_user.id in matched_users or next_user.id in [u.id for u in current_path]:
                continue
            
            for item in current_user.offered_items:
                if item.id in matched_items:
                    continue
                
                if item in next_user.desired_items:
                    # Encontrar un item que next_user ofrezca y alguien quiera
                    for next_item in next_user.offered_items:
                        if next_item.id in matched_items:
                            continue
                        
                        new_path = current_path + [next_user]
                        new_items = current_items + [next_item]
                        
                        result_path, result_items = find_cycle(
                            start_user, new_path, new_items, depth + 1
                        )
                        
                        if result_path:
                            return result_path, result_items
        
        return None, None
    
    for user in users:
        if user.id in matched_users:
            continue
        
        cycle_path, cycle_items = find_cycle(user, [user], [], 1)
        if cycle_path and cycle_items:
            matches.append({
                "participants": [u.id for u in cycle_path],
                "items": [item.id for item in cycle_items]
            })
            matched_users.update([u.id for u in cycle_path])
            matched_items.update([item.id for item in cycle_items])
    
    return matches

# ========== CREACIÓN DE DATOS ==========

def create_test_users(n=100, density=0.3):
    """Crear usuarios con densidad de matching controlada"""
    users = []
    categories = ['electronics', 'clothing', 'books', 'home', 'sports']
    levels = [UserLevel.NOVATO, UserLevel.MIEMBRO, UserLevel.CONFIABLE, UserLevel.ELITE]
    
    # Primero crear todos los usuarios y items
    all_items = []
    for i in range(n):
        level = random.choice(levels)
        user = User(
            id=f'user_{i}',
            name=f'User {i}',
            level=level,
            reputation=random.uniform(500, 1000) if level.value >= 3 else random.uniform(0, 500),
            offered_items=[],
            desired_items=[]
        )
        
        # 1-3 items ofrecidos
        num_offered = random.randint(1, 3)
        for j in range(num_offered):
            item = Item(
                id=f'item_{i}_{j}',
                name=f'{random.choice(categories)} item {j}',
                value=random.uniform(50, 500),
                category=random.choice(categories)
            )
            user.offered_items.append(item)
            all_items.append((item, user))
        
        users.append(user)
    
    # Crear deseos cruzados con densidad controlada
    for user in users:
        # Número de deseos basado en densidad
        num_desires = max(1, int(len(all_items) * density / n))
        
        for _ in range(num_desires):
            # Escoger un item de otro usuario
            item, owner = random.choice([(i, o) for i, o in all_items if o != user])
            if item not in user.desired_items:
                user.desired_items.append(item)
    
    return users

# ========== PROFILING ==========

def profile_algorithm():
    print("="*70)
    print("PROFILING DEL ALGORITMO ACTUAL")
    print("="*70)
    
    test_sizes = [50, 100, 150]
    results = {}
    
    for n in test_sizes:
        print(f"\n=== TEST CON {n} USUARIOS ===")
        
        # Crear datos
        start = time.time()
        users = create_test_users(n, density=0.3)
        creation_time = time.time() - start
        print(f"Creación datos: {creation_time:.3f}s")
        
        # k=2
        start = time.time()
        matches_k2 = find_direct_matches_naive(users)
        time_k2 = time.time() - start
        print(f"k=2: {time_k2:.3f}s, Matches: {len(matches_k2)}")
        
        # k=3
        start = time.time()
        matches_k3 = find_circular_matches_naive(users, k=3)
        time_k3 = time.time() - start
        print(f"k=3: {time_k3:.3f}s, Matches: {len(matches_k3)}")
        
        # k=4 (con timeout)
        start = time.time()
        try:
            # Para n grande, limitar tiempo
            if n >= 100:
                print("k=4: Probando con timeout de 30s...")
                import signal
                class TimeoutException(Exception):
                    pass
                
                def timeout_handler(signum, frame):
                    raise TimeoutException()
                
                # Configurar timeout
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(30)
                
                try:
                    matches_k4 = find_circular_matches_naive(users, k=4)
                    time_k4 = time.time() - start
                    print(f"k=4: {time_k4:.3f}s, Matches: {len(matches_k4)}")
                except TimeoutException:
                    time_k4 = 30.0
                    matches_k4 = []
                    print(f"k=4: TIMEOUT (>30s)")
                finally:
                    signal.alarm(0)
            else:
                matches_k4 = find_circular_matches_naive(users, k=4)
                time_k4 = time.time() - start
                print(f"k=4: {time_k4:.3f}s, Matches: {len(matches_k4)}")
        except Exception as e:
            time_k4 = time.time() - start
            print(f"k=4: ERROR después de {time_k4:.1f}s - {e}")
            matches_k4 = []
        
        results[n] = {
            'k2_time': time_k2,
            'k2_matches': len(matches_k2),
            'k3_time': time_k3,
            'k3_matches': len(matches_k3),
            'k4_time': time_k4,
            'k4_matches': len(matches_k4),
            'k3_vs_k2': time_k3 / time_k2 if time_k2 > 0 else float('inf'),
            'k4_vs_k2': time_k4 / time_k2 if time_k2 > 0 else float('inf')
        }
    
    # Análisis
    print("\n" + "="*70)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("="*70)
    
    for n in test_sizes:
        r = results[n]
        print(f"\n{n} usuarios:")
        print(f"  k=2: {r['k2_time']:.3f}s ({r['k2_matches']} matches)")
        print(f"  k=3: {r['k3_time']:.3f}s ({r['k3_vs_k2']:.1f}x más lento)")
        print(f"  k=4: {r['k4_time']:.3f}s ({r['k4_vs_k2']:.1f}x más lento)")
    
    # Estimación para 100 usuarios
    print("\n" + "="*70)
    print("ESTIMACIÓN PARA 100 USUARIOS (EXTRAPOLACIÓN)")
    print("="*70)
    
    if 100 in results:
        r = results[100]
        print(f"Tiempo actual k=4: {r['k4_time']:.1f}s")
        
        # Objetivo: reducir 200% (hacer 3x más rápido)
        target_time = r['k4_time'] / 3
        print(f"Objetivo después de optimización: {target_time:.1f}s")
        print(f"Reducción necesaria: {r['k4_time'] - target_time:.1f}s")
    
    return results

# ========== ANÁLISIS DE CUELOS DE BOTELLA ==========

def analyze_bottlenecks():
    print("\n" + "="*70)
    print("ANÁLISIS DE CUELOS DE BOTELLA")
    print("="*70)
    
    # Crear dataset pequeño para profiling detallado
    users = create_test_users(30, density=0.4)
    
    import cProfile
    import pstats
    from io import StringIO
    
    print("\nProfiling k=3 (30 usuarios):")
    pr = cProfile.Profile()
    pr.enable()
    matches = find_circular_matches_naive(users, k=3)
    pr.disable()
    
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())
    
    print("\nPrincipales cuellos de botella identificados:")
    print("1. Búsqueda recursiva exhaustiva O(n^k)")
    print("2. Verificaciones de membresía en listas (O(n))")
    print("3. No hay pruning temprano")
    print("4. No hay caching de compatibilidad")
    print("5. No hay paralelización")

if __name__ == "__main__":
    results = profile_algorithm()
    analyze_bottlenecks()
    
    # Guardar resultados
    with open("profiling_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResultados guardados en profiling_results.json")