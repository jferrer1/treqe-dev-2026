#!/usr/bin/env python3
"""
ALGORITMO TREQE V1.0 - Versión Windows (sin Unicode)
Algoritmo ascendente k=2 → k_max con timeout inteligente
"""

import time
import random
import sys
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque

class TreqeUser:
    """Usuario de la plataforma Treqe"""
    def __init__(self, user_id: int, offered_item: str, offered_value: float, 
                 wanted_items: List[str], wanted_values: List[float]):
        self.id = user_id
        self.offered = {
            'item': offered_item,
            'value': offered_value,
            'owner': user_id
        }
        self.wanted = [
            {'item': item, 'value': value, 'owner': None}
            for item, value in zip(wanted_items, wanted_values)
        ]
        self.flexibility = random.uniform(0.3, 0.8)
        
    def __repr__(self):
        return f"User({self.id}, offers:{self.offered['item']}, wants:{len(self.wanted)} items)"

class TreqeAscendingAlgorithm:
    """
    Algoritmo ascendente para Treqe
    k=2 → k_max con timeout inteligente
    """
    
    def __init__(self, time_budget_seconds: int = 300, max_k: int = 8):
        self.time_budget = time_budget_seconds
        self.max_k = max_k
        self.start_time = None
        self.users = []
        
    def create_realistic_users(self, n_users: int = 100) -> List[TreqeUser]:
        """Crear usuarios realistas con preferencias múltiples"""
        items_pool = [
            "iPhone 15 Pro", "Samsung S24", "MacBook Pro M3", "iPad Air",
            "Canon EOS R5", "Sony A7IV", "Nintendo Switch", "PlayStation 5",
            "Zapatos Nike", "Chaqueta North Face", "Bolso Michael Kors", "Reloj Casio",
            "Sofa 3 plazas", "Mesa comedor", "Lampara diseño", "Vajilla completa",
            "Bicicleta carretera", "Cinta correr", "Raqueta tenis", "Pesas 20kg",
            "Libro bestseller", "Vinilo colección", "Juego mesa", "Herramientas"
        ]
        
        item_values = {
            "iPhone 15 Pro": 900, "Samsung S24": 800, "MacBook Pro M3": 1800,
            "iPad Air": 600, "Canon EOS R5": 2500, "Sony A7IV": 2200,
            "Nintendo Switch": 250, "PlayStation 5": 450,
            "Zapatos Nike": 80, "Chaqueta North Face": 120, 
            "Bolso Michael Kors": 150, "Reloj Casio": 60,
            "Sofa 3 plazas": 300, "Mesa comedor": 200, 
            "Lampara diseño": 80, "Vajilla completa": 100,
            "Bicicleta carretera": 400, "Cinta correr": 350,
            "Raqueta tenis": 70, "Pesas 20kg": 50,
            "Libro bestseller": 15, "Vinilo colección": 30,
            "Juego mesa": 40, "Herramientas": 60
        }
        
        users = []
        for user_id in range(n_users):
            offered_item = random.choice(items_pool)
            offered_value = item_values[offered_item]
            
            n_wanted = random.randint(1, 5)
            available_items = [item for item in items_pool if item != offered_item]
            wanted_items = random.sample(available_items, min(n_wanted, len(available_items)))
            wanted_values = [item_values[item] for item in wanted_items]
            
            users.append(TreqeUser(user_id, offered_item, offered_value, wanted_items, wanted_values))
        
        return users
    
    def build_preference_graph(self, users: List[TreqeUser]) -> Dict[int, Set[int]]:
        """Construir grafo de preferencias: usuario -> usuarios que tienen items que quiere"""
        graph = defaultdict(set)
        item_to_owners = defaultdict(set)
        
        # Mapear cada item a sus dueños
        for user in users:
            item_to_owners[user.offered['item']].add(user.id)
        
        # Construir grafo: usuario A quiere items de usuario B
        for user in users:
            user_id = user.id
            for wanted in user.wanted:
                item = wanted['item']
                if item in item_to_owners:
                    for owner_id in item_to_owners[item]:
                        if owner_id != user_id:
                            graph[user_id].add(owner_id)
        
        return graph
    
    def estimate_time_for_k(self, k: int, n_users: int, n_matched: int) -> float:
        """Estimar tiempo necesario para buscar ciclos de tamaño k"""
        remaining_users = n_users - n_matched
        if remaining_users < k:
            return 0
        
        base_time = 0.001
        combinations = (remaining_users ** (k/2)) / 1000
        estimated = base_time * combinations
        
        return min(estimated, 60)
    
    def find_cycles_k(self, graph: Dict[int, Set[int]], k: int, 
                     matched_users: Set[int], time_remaining: float) -> List[List[int]]:
        """Encontrar todos los ciclos simples de tamaño k usando BFS limitado por tiempo"""
        if k < 2:
            return []
        
        cycles = []
        start_time = time.time()
        
        available_users = [uid for uid in graph.keys() if uid not in matched_users]
        
        # Para k=2, búsqueda directa
        if k == 2:
            for u1 in available_users:
                if time.time() - start_time > time_remaining * 0.5:
                    break
                for u2 in graph.get(u1, set()):
                    if u2 not in matched_users and u1 in graph.get(u2, set()):
                        cycles.append([u1, u2])
            return cycles
        
        # Para k>2, BDFS limitado
        for start in available_users:
            if time.time() - start_time > time_remaining * 0.5:
                break
            
            stack = [(start, [start], {start})]
            
            while stack:
                current, path, visited = stack.pop()
                
                if time.time() - start_time > time_remaining * 0.5:
                    break
                
                if len(path) == k:
                    if start in graph.get(current, set()):
                        cycles.append(path.copy())
                    continue
                
                for neighbor in graph.get(current, set()):
                    if neighbor not in visited and neighbor not in matched_users:
                        new_path = path + [neighbor]
                        new_visited = visited | {neighbor}
                        stack.append((neighbor, new_path, new_visited))
        
        return cycles
    
    def select_non_overlapping_cycles(self, cycles: List[List[int]], 
                                     matched_users: Set[int]) -> List[List[int]]:
        """Selección greedy de ciclos no solapados"""
        if not cycles:
            return []
        
        cycles.sort(key=lambda x: len(x), reverse=True)
        
        selected = []
        used_in_selected = set()
        
        for cycle in cycles:
            cycle_set = set(cycle)
            if not cycle_set.intersection(used_in_selected) and not cycle_set.intersection(matched_users):
                selected.append(cycle)
                used_in_selected.update(cycle_set)
        
        return selected
    
    def calculate_cycle_value(self, cycle: List[int], users: List[TreqeUser]) -> float:
        """Calcular valor total intercambiado en un ciclo"""
        total_value = 0
        
        for i in range(len(cycle)):
            current_user = users[cycle[i]]
            next_user = users[cycle[(i + 1) % len(cycle)]]
            
            for wanted in current_user.wanted:
                if wanted['item'] == next_user.offered['item']:
                    total_value += wanted['value']
                    break
        
        return total_value
    
    def run_ascending_algorithm(self, n_users: int = 100, verbose: bool = True) -> Dict:
        """Ejecutar algoritmo ascendente k=2 -> k_max"""
        self.start_time = time.time()
        
        self.users = self.create_realistic_users(n_users)
        
        if verbose:
            print("="*70)
            print("ALGORITMO TREQE ASCENDENTE V1.0")
            print(f"Usuarios: {n_users}, Timeout: {self.time_budget}s, k maximo: {self.max_k}")
            print("="*70)
        
        graph_start = time.time()
        graph = self.build_preference_graph(self.users)
        graph_time = time.time() - graph_start
        
        total_edges = sum(len(neighbors) for neighbors in graph.values())
        density = total_edges / (n_users * (n_users - 1)) * 100 if n_users > 1 else 0
        
        if verbose:
            print("\n1. Construyendo grafo de preferencias...")
            print(f"   * Usuarios: {n_users}")
            print(f"   * Aristas: {total_edges}")
            print(f"   * Densidad: {density:.2f}%")
            print(f"   * Tiempo construccion: {graph_time:.3f}s")
        
        matched_user_ids = set()
        results_by_k = {}
        execution_stats = {}
        
        if verbose:
            print("\n2. Buscando matches (k=2 hasta k_max)...")
            print("   " + "-"*50)
        
        for k in range(2, self.max_k + 1):
            elapsed = time.time() - self.start_time
            if elapsed >= self.time_budget:
                if verbose:
                    print(f"   [TIMEOUT] Timeout alcanzado ({elapsed:.1f}s)")
                break
            
            remaining_users = n_users - len(matched_user_ids)
            if remaining_users < k:
                if verbose:
                    print(f"   [PARAR] k={k}: No hay suficientes usuarios ({remaining_users} < {k})")
                break
            
            estimated_time = self.estimate_time_for_k(k, n_users, len(matched_user_ids))
            time_remaining = self.time_budget - elapsed
            
            if estimated_time > time_remaining * 0.8:
                if verbose:
                    print(f"   [SALTAR] k={k}: Estimado {estimated_time:.1f}s > {time_remaining*0.8:.1f}s, saltando")
                continue
            
            if verbose:
                print(f"   [BUSCAR] k={k}: Buscando ciclos ({remaining_users} usuarios disponibles)...")
            
            cycle_start = time.time()
            all_cycles = self.find_cycles_k(graph, k, matched_user_ids, time_remaining)
            cycle_time = time.time() - cycle_start
            
            if not all_cycles:
                if verbose:
                    print(f"      * Ciclos encontrados: 0")
                execution_stats[k] = {'cycles_found': 0, 'cycles_selected': 0, 'time': cycle_time}
                continue
            
            selected_cycles = self.select_non_overlapping_cycles(all_cycles, matched_user_ids)
            
            for cycle in selected_cycles:
                matched_user_ids.update(cycle)
            
            total_value = sum(self.calculate_cycle_value(cycle, self.users) for cycle in selected_cycles)
            avg_value_per_user = total_value / (len(selected_cycles) * k) if selected_cycles else 0
            
            if verbose:
                print(f"      * Ciclos encontrados: {len(all_cycles)}")
                print(f"      * Ciclos seleccionados: {len(selected_cycles)}")
                print(f"      * Usuarios emparejados: +{len(selected_cycles) * k}")
                print(f"      * Valor total: EUR{total_value:.0f}")
                print(f"      * Valor/usuario: EUR{avg_value_per_user:.0f}")
                print(f"      * Tiempo busqueda: {cycle_time:.3f}s")
            
            results_by_k[k] = selected_cycles
            execution_stats[k] = {
                'cycles_found': len(all_cycles),
                'cycles_selected': len(selected_cycles),
                'users_matched': len(selected_cycles) * k,
                'total_value': total_value,
                'avg_value_per_user': avg_value_per_user,
                'time': cycle_time
            }
        
        total_time = time.time() - self.start_time
        coverage = len(matched_user_ids) / n_users * 100 if n_users > 0 else 0
        
        if verbose:
            print("\n" + "="*70)
            print("RESUMEN EJECUTIVO:")
            print("="*70)
            
            print(f"* Usuarios procesados: {n_users}")
            print(f"* Usuarios emparejados: {len(matched_user_ids)} ({coverage:.1f}%)")
            print(f"* Tiempo total: {total_time:.2f}s")
            
            if results_by_k:
                max_k_used = max(results_by_k.keys())
                print(f"* k maximo utilizado: {max_k_used}")
            
            print(f"\n* DISTRIBUCION POR k:")
            for k in sorted(execution_stats.keys()):
                stats = execution_stats[k]
                if 'users_matched' in stats:
                    print(f"  k={k}: {stats['cycles_selected']} ciclos, {stats['users_matched']} usuarios, EUR{stats['total_value']:.0f}")
                else:
                    print(f"  k={k}: {stats['cycles_selected']} ciclos, 0 usuarios, EUR0")
            
            print(f"\n* VIABILIDAD:")
            if coverage >= 70:
                print("  [OK] VIABLE - Cobertura >70% alcanzada")
            elif coverage >= 50:
                print("  [WARNING] MARGINAL - Cobertura 50-70%, necesita optimizacion")
            else:
                print("  [ERROR] NO VIABLE - Cobertura <50%, revisar algoritmo")
        
        return {
            'users': self.users,
            'matched_user_ids': matched_user_ids,
            'coverage': coverage,
            'total_time': total_time,
            'results_by_k': results_by_k,
            'execution_stats': execution_stats,
            'graph_density': density
        }

def main():
    """Funcion principal para ejecutar el algoritmo"""
    print("ALGORITMO TREQE - IMPLEMENTACION V1.0 (Windows)")
    print("Algoritmo ascendente k=2 -> k_max con timeout inteligente")
    print()
    
    n_users = 100
    time_budget = 300
    max_k = 8
    
    print(f"Configuracion:")
    print(f"  * Usuarios: {n_users}")
    print(f"  * Timeout: {time_budget}s (5 minutos)")
    print(f"  * k maximo: {max_k}")
    print()
    
    algorithm = TreqeAscendingAlgorithm(time_budget_seconds=time_budget, max_k=max_k)
    result = algorithm.run_ascending_algorithm(n_users=n_users, verbose=True)
    
    print("\n" + "="*70)
    print("RECOMENDACIONES PARA PRODUCCION:")
    print("="*70)
    
    print(f"1. Ejecutar cada: 10 minutos")
    print(f"2. Timeout: {time_budget} segundos")
    print(f"3. k maximo inicial: {max_k}")
    print(f"4. Esperar cobertura: {result['coverage']:.1f}%")
    print(f"5. Densidad del grafo: {result['graph_density']:.2f}%")
    
    if result['coverage'] >= 70:
        print("\n[OK] El algoritmo es VIABLE para implementacion en produccion")
    else:
        print("\n[WARNING] El algoritmo necesita optimizacion")

if __name__ == "__main__":
    main()