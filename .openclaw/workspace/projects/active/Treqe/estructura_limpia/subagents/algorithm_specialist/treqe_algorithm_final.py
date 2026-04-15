#!/usr/bin/env python3
"""
ALGORITMO TREQE FINAL - Ascendente k=2→k_max con timeout 5 minutos
"""

import time
import random
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque
import heapq

class TreqeUser:
    """Usuario de Treqe"""
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
    Algoritmo ascendente: k=2 → k_max con timeout
    """
    
    def __init__(self, time_budget_seconds: int = 300, max_k: int = 10):
        self.time_budget = time_budget_seconds
        self.max_k = max_k
        self.start_time = None
        self.users = []
        
    def create_test_users(self, n_users: int = 100) -> List[TreqeUser]:
        """Crear usuarios de prueba realistas"""
        items_pool = [
            "iPhone 15 Pro", "Samsung S24", "MacBook Pro M3", "iPad Air",
            "Canon EOS R5", "Sony A7IV", "Nintendo Switch", "PlayStation 5",
            "Zapatos Nike", "Chaqueta North Face", "Bolso Michael Kors", 
            "Sofa 3 plazas", "Mesa comedor", "Bicicleta carretera", "Cinta correr"
        ]
        
        item_values = {
            "iPhone 15 Pro": 900, "Samsung S24": 800, "MacBook Pro M3": 1800,
            "iPad Air": 600, "Canon EOS R5": 2500, "Sony A7IV": 2200,
            "Nintendo Switch": 250, "PlayStation 5": 450,
            "Zapatos Nike": 80, "Chaqueta North Face": 120, 
            "Bolso Michael Kors": 150, "Sofa 3 plazas": 300,
            "Mesa comedor": 200, "Bicicleta carretera": 400,
            "Cinta correr": 350
        }
        
        users = []
        for user_id in range(n_users):
            offered_item = random.choice(items_pool)
            offered_value = item_values[offered_item]
            
            # Usuario quiere 1-3 items
            n_wanted = random.randint(1, 3)
            available_items = [item for item in items_pool if item != offered_item]
            wanted_items = random.sample(available_items, min(n_wanted, len(available_items)))
            wanted_values = [item_values[item] for item in wanted_items]
            
            users.append(TreqeUser(user_id, offered_item, offered_value, wanted_items, wanted_values))
        
        return users
    
    def build_preference_graph(self, users: List[TreqeUser]) -> Dict[int, Set[int]]:
        """Construir grafo de preferencias: usuario → usuarios que tienen items que quiere"""
        graph = defaultdict(set)
        item_to_owners = defaultdict(set)
        
        # Mapear cada item a sus dueños
        for user in users:
            item_to_owners[user.offered['item']].add(user.id)
        
        # Construir grafo
        for user in users:
            user_id = user.id
            for wanted in user.wanted:
                item = wanted['item']
                if item in item_to_owners:
                    for owner_id in item_to_owners[item]:
                        if owner_id != user_id:  # No puede querer su propio item
                            graph[user_id].add(owner_id)
        
        return graph
    
    def estimate_time_for_k(self, k: int, n_users: int, n_matched: int) -> float:
        """
        Estimar tiempo necesario para buscar ciclos de tamaño k
        Fórmula empírica: O((n-m)^(k/2))
        """
        remaining_users = n_users - n_matched
        if remaining_users < k:
            return 0.0
            
        # Caso base: k=2 es O((n-m)²)
        base_time_per_pair = 0.00001  # segundos por par verificado
        complexity = remaining_users ** (k / 2.0)
        
        return base_time_per_pair * complexity
    
    def find_cycles_k(self, graph: Dict[int, Set[int]], k: int, 
                     excluded_users: Set[int], time_remaining: float) -> List[Tuple[int, ...]]:
        """
        Encontrar ciclos de tamaño k usando DFS limitada
        """
        if k < 2:
            return []
            
        all_users = set(graph.keys())
        available_users = all_users - excluded_users
        available_users_list = list(available_users)
        
        if len(available_users_list) < k:
            return []
        
        cycles = []
        start_search_time = time.time()
        
        # Para cada usuario como punto de inicio
        for start_idx, start_user in enumerate(available_users_list):
            # Verificar timeout
            if time.time() - start_search_time > time_remaining:
                break
                
            # DFS limitada a profundidad k-1
            stack = [(start_user, [start_user], set([start_user]))]
            
            while stack:
                current_user, path, visited = stack.pop()
                
                # Si llegamos al tamaño k
                if len(path) == k:
                    # Verificar si cierra ciclo
                    last_user = path[-1]
                    if start_user in graph.get(last_user, set()):
                        # Verificar que todos usuarios diferentes
                        if len(set(path)) == k:
                            # Normalizar ciclo (empezar por mínimo)
                            min_idx = path.index(min(path))
                            normalized = tuple(path[min_idx:] + path[:min_idx])
                            if normalized not in cycles:
                                cycles.append(normalized)
                    continue
                
                # Continuar búsqueda si no llegamos a k
                if len(path) < k:
                    neighbors = graph.get(current_user, set())
                    for neighbor in neighbors:
                        if neighbor not in visited and neighbor not in excluded_users:
                            new_path = path + [neighbor]
                            new_visited = visited.copy()
                            new_visited.add(neighbor)
                            stack.append((neighbor, new_path, new_visited))
        
        return cycles
    
    def select_non_overlapping_cycles(self, cycles: List[Tuple[int, ...]], 
                                    already_matched: Set[int]) -> List[Tuple[int, ...]]:
        """Selección greedy de ciclos no solapados"""
        selected = []
        used_in_selected = set()
        
        # Ordenar ciclos por tamaño (k más pequeño primero) y luego por "calidad"
        cycles_sorted = sorted(cycles, key=lambda c: (len(c), -sum(c)))  # k pequeño, suma alta
        
        for cycle in cycles_sorted:
            cycle_users = set(cycle)
            # Verificar que no solape con ciclos ya seleccionados
            if not cycle_users.intersection(used_in_selected) and not cycle_users.intersection(already_matched):
                selected.append(cycle)
                used_in_selected.update(cycle_users)
        
        return selected
    
    def calculate_cycle_value(self, cycle: Tuple[int, ...], users: List[TreqeUser]) -> float:
        """Calcular valor total de un ciclo"""
        total_value = 0.0
        user_dict = {user.id: user for user in users}
        
        for i in range(len(cycle)):
            user_from_id = cycle[i]
            user_to_id = cycle[(i + 1) % len(cycle)]
            
            user_from = user_dict[user_from_id]
            user_to = user_dict[user_to_id]
            
            # Buscar qué item quiere user_from de user_to
            for wanted in user_from.wanted:
                if user_to.offered['item'] == wanted['item']:
                    total_value += wanted['value']
                    break
        
        return total_value
    
    def run_ascending_algorithm(self, users: Optional[List[TreqeUser]] = None, 
                               n_users: int = 100) -> Dict:
        """
        Ejecutar algoritmo ascendente k=2→k_max
        """
        self.start_time = time.time()
        
        # Crear usuarios si no se proporcionan
        if users is None:
            self.users = self.create_test_users(n_users)
        else:
            self.users = users
        
        print("="*70)
        print(f"ALGORITMO TREQE ASCENDENTE - {len(self.users)} usuarios")
        print(f"Timeout: {self.time_budget}s, k máximo: {self.max_k}")
        print("="*70)
        
        # Construir grafo de preferencias
        print("\n1. Construyendo grafo de preferencias...")
        graph_start = time.time()
        graph = self.build_preference_graph(self.users)
        graph_time = time.time() - graph_start
        
        total_edges = sum(len(neighbors) for neighbors in graph.values())
        print(f"   • Usuarios: {len(self.users)}")
        print(f"   • Aristas: {total_edges}")
        print(f"   • Densidad: {total_edges/(len(self.users)*(len(self.users)-1))*100:.2f}%")
        print(f"   • Tiempo construcción: {graph_time:.3f}s")
        
        # Variables de estado
        matched_user_ids = set()
        results_by_k = {}
        execution_stats = {}
        
        print("\n2. Buscando matches (k=2 hasta k_max)...")
        print("   " + "-"*50)
        
        # Bucle principal: k desde 2 hasta max_k
        for k in range(2, self.max_k + 1):
            # Verificar timeout
            elapsed = time.time() - self.start_time
            if elapsed >= self.time_budget:
                print(f"   [TIMEOUT] Timeout alcanzado ({elapsed:.1f}s)")
                break
            
            # Verificar si hay suficientes usuarios no emparejados
            remaining_users = len(self.users) - len(matched_user_ids)
            if remaining_users < k:
                print(f"   [PARAR] k={k}: No hay suficientes usuarios ({remaining_users} < {k})")
                break
            
            # Estimar tiempo para este k
            estimated_time = self.estimate_time_for_k(k, len(self.users), len(matched_user_ids))
            time_remaining = self.time_budget - elapsed
            
            if estimated_time > time_remaining * 0.8:  # 80% del tiempo restante
                print(f"   [SALTAR] k={k}: Estimado {estimated_time:.1f}s > {time_remaining*0.8:.1f}s, saltando")
                continue
            
            print(f"   [BUSCAR] k={k}: Buscando ciclos ({remaining_users} usuarios disponibles)...")
            
            # Buscar ciclos de tamaño k
            cycle_start = time.time()
            all_cycles = self.find_cycles_k(graph, k, matched_user_ids, time_remaining)
            cycle_time = time.time() - cycle_start
            
            if not all_cycles:
                print(f"      * Ciclos encontrados: 0")
                execution_stats[k] = {'cycles_found': 0, 'cycles_selected': 0, 'time': cycle_time}
                continue
            
            # Seleccionar ciclos no solapados
            selected_cycles = self.select_non_overlapping_cycles(all_cycles, matched_user_ids)
            
            # Actualizar usuarios emparejados
            for cycle in selected_cycles:
                matched_user_ids.update(cycle)
            
            # Calcular estadísticas
            total_value = sum(self.calculate_cycle_value(cycle, self.users) for cycle in selected_cycles)
            avg_value_per_user = total_value / (len(selected_cycles) * k) if selected_cycles else 0
            
            print(f"      * Ciclos encontrados: {len(all_cycles)}")
            print(f"      * Ciclos seleccionados: {len(selected_cycles)}")
            print(f"      * Usuarios emparejados: +{len(selected_cycles) * k}")
            print(f"      * Valor total: EUR{total_value:.0f}")
            print(f"      * Valor/usuario: EUR{avg_value_per_user:.0f}")
            print(f"      * Tiempo busqueda: {cycle_time:.3f}s")
            
            # Guardar resultados
            results_by_k[k] = selected_cycles
            execution_stats[k] = {
                'cycles_found': len(all_cycles),
                'cycles_selected': len(selected_cycles),
                'users_matched': len(selected_cycles) * k,
                'total_value': total_value,
                'avg_value_per_user': avg_value_per_user,
                'time': cycle_time
            }
        
        # Resultados finales
        total_time = time.time() - self.start_time
        coverage = len(matched_user_ids) / len(self.users) * 100
        
        print("\n" + "="*70)
        print("RESULTADOS FINALES")
        print("="*70)
        
        print(f"\n* Tiempo total: {total_time:.2f}s (de {self.time_budget}s)")
        print(f"* Usuarios emparejados: {len(matched_user_ids)}/{len(self.users)} ({coverage:.1f}%)")
        print(f"* k maximo alcanzado: {max(results_by_k.keys()) if results_by_k else 0}")
        
        # Resumen por k
        print(f"\n* RESUMEN POR k:")
        print("  " + "-"*40)
        for k in sorted(results_by_k.keys()):
            stats = execution_stats[k]
            cycles = results_by_k[k]
            print(f"  k={k}: {len(cycles)} ciclos, {stats['users_matched']} usuarios, EUR{stats['total_value']:.0f} valor")
        
        # Ejemplos de ciclos encontrados
        print(f"\n* EJEMPLOS DE CICLOS ENCONTRADOS:")
        print("  " + "-"*40)
        
        example_count = 0
        for k, cycles in results_by_k.items():
            for i, cycle in enumerate(cycles[:2]):  # Mostrar 2 por k
                if example_count >= 5:
                    break
                    
                value = self.calculate_cycle_value(cycle, self.users)
                print(f"  Ciclo k={k} (EUR{value:.0f}): {cycle}")
                
                # Mostrar intercambio
                print("    Intercambio:")
                for j in range(k):
                    user_from_id = cycle[j]
                    user_to_id = cycle[(j + 1) % k]
                    user_from = self.users[user_from_id]
                    user_to = self.users[user_to_id]
                    print(f"      {user_from_id}->{user_to_id}: {user_from.offered['item']}")
                
                example_count += 1
                if example_count >= 5:
                    break
        
        # Recomendaciones
        print(f"\n* RECOMENDACIONES:")
        print("  " + "-"*40)
        
        if coverage >= 80:
            print(f"  [OK] COBERTURA EXCELENTE ({coverage:.1f}%)")
            print(f"  * Algoritmo funciona bien para {len(self.users)} usuarios")
            print(f"  * k maximo util: {max(results_by_k.keys())}")
        elif coverage >= 50:
            print(f"  [ALERTA] COBERTURA ACEPTABLE ({coverage:.1f}%)")
            print(f"  * Considerar aumentar tiempo o optimizar algoritmo")
            print(f"  * k mas efectivo: {max(results_by_k.keys(), key=lambda k: execution_stats[k]['users_matched'])}")
        else:
            print(f"  [PROBLEMA] COBERTURA BAJA ({coverage:.1f}%)")
            print(f"  * Revisar densidad de preferencias")
            print(f"  * Considerar k mas alto o mas tiempo")
        
        # Para batch processing
        print(f"\n* CONFIGURACION BATCH RECOMENDADA:")
        print("  " + "-"*40)
        print(f"  * Ejecutar cada: 10 minutos")
        print(f"  * Timeout algoritmo: {min(total_time * 1.5, 300):.0f}s")
        print(f"  * k maximo inicial: {min(self.max_k, max(results_by_k.keys()) + 2 if results_by_k else 4)}")
        print(f"  * Usuarios por batch: {len(self.users)}")
        
        return {
            'users': self.users,
            'matched_user_ids': matched_user_ids,
            'results_by_k': results_by_k,
            'execution_stats': execution_stats,
            'total_time': total_time,
            'coverage': coverage,
            'graph': graph
        }