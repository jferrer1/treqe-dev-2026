#!/usr/bin/env python3
"""
ALGORITMO TREQE FINAL - Sin emojis para Windows
"""

import numpy as np
import time
from typing import List, Dict, Set, Tuple
import random
from collections import defaultdict, deque

class TreqeFinalAlgorithm:
    """
    Algoritmo FINAL para Treqe - Entendimiento CORRECTO:
    - k>2 RESUELVE matching asimétrico
    - Más usuarios = más formas de cerrar ciclos
    - Usuarios seleccionan múltiples items que les gustan
    """
    
    def __init__(self, n_users=100, avg_preferences=3, k_max=4):
        self.n_users = n_users
        self.avg_preferences = avg_preferences
        self.k_max = k_max
        self.users = self._create_realistic_users()
        
    def _create_realistic_users(self):
        """Crea usuarios realistas con preferencias múltiples"""
        users = []
        
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
        
        for user_id in range(self.n_users):
            offered_item = random.choice(items_pool)
            offered_value = item_values[offered_item]
            
            n_wanted = random.randint(1, 5)
            available_items = [item for item in items_pool if item != offered_item]
            wanted_items = random.sample(available_items, min(n_wanted, len(available_items)))
            wanted_values = [item_values[item] for item in wanted_items]
            
            users.append({
                'id': user_id,
                'offered': {'item': offered_item, 'value': offered_value, 'owner': user_id},
                'wanted': [
                    {'item': item, 'value': value, 'owner': None}
                    for item, value in zip(wanted_items, wanted_values)
                ],
                'flexibility': random.uniform(0.3, 0.8)
            })
        
        return users
    
    def build_preference_graph(self):
        """Construye grafo de preferencias"""
        graph = defaultdict(lambda: {'owners': set(), 'items': {}})
        item_to_owners = defaultdict(set)
        
        for user in self.users:
            item_to_owners[user['offered']['item']].add(user['id'])
        
        for user in self.users:
            user_id = user['id']
            for wanted in user['wanted']:
                item = wanted['item']
                if item in item_to_owners:
                    for owner_id in item_to_owners[item]:
                        if owner_id != user_id:
                            graph[user_id]['owners'].add(owner_id)
                            graph[user_id]['items'][owner_id] = item
        
        return graph
    
    def find_cycles_optimized(self, graph, k_values=[2, 3, 4]):
        """Encuentra ciclos de diferentes tamaños"""
        cycles_by_k = {k: [] for k in k_values}
        
        for start_user in range(self.n_users):
            for k in k_values:
                if k < 2:
                    continue
                    
                stack = [(start_user, [start_user], set([start_user]))]
                
                while stack:
                    current_user, path, visited = stack.pop()
                    
                    if len(path) == k:
                        last_user = path[-1]
                        last_user_data = graph.get(last_user, {})
                        if 'owners' in last_user_data and start_user in last_user_data['owners']:
                            cycle = path[:]
                            if len(set(cycle)) == k:
                                normalized_cycle = self._normalize_cycle(cycle)
                                if normalized_cycle not in cycles_by_k[k]:
                                    cycles_by_k[k].append(normalized_cycle)
                        continue
                    
                    if len(path) < k:
                        current_user_data = graph.get(current_user, {})
                        if 'owners' in current_user_data:
                            for neighbor in current_user_data['owners']:
                                if neighbor not in visited:
                                    new_path = path + [neighbor]
                                    new_visited = visited.copy()
                                    new_visited.add(neighbor)
                                    stack.append((neighbor, new_path, new_visited))
        
        return cycles_by_k
    
    def _normalize_cycle(self, cycle):
        """Normaliza ciclo para evitar duplicados"""
        min_idx = cycle.index(min(cycle))
        normalized = cycle[min_idx:] + cycle[:min_idx]
        return tuple(normalized)
    
    def calculate_cycle_value(self, cycle):
        """Calcula valor económico de un ciclo"""
        total_value = 0
        
        for i in range(len(cycle)):
            user_from = cycle[i]
            user_to = cycle[(i + 1) % len(cycle)]
            
            for wanted in self.users[user_from]['wanted']:
                if self.users[user_to]['offered']['item'] == wanted['item']:
                    total_value += wanted['value']
                    break
        
        return total_value
    
    def greedy_cycle_selection(self, cycles_by_k, max_cycles=100):
        """Selección greedy de ciclos"""
        selected_cycles = []
        used_users = set()
        total_value = 0
        
        all_cycles = []
        for k, cycles in cycles_by_k.items():
            for cycle in cycles:
                value = self.calculate_cycle_value(cycle)
                efficiency = value / k
                all_cycles.append((cycle, k, value, efficiency))
        
        all_cycles.sort(key=lambda x: x[3], reverse=True)
        
        for cycle, k, value, efficiency in all_cycles:
            cycle_users = set(cycle)
            if not cycle_users.intersection(used_users):
                selected_cycles.append({
                    'cycle': cycle,
                    'k': k,
                    'value': value,
                    'efficiency': efficiency,
                    'users': list(cycle_users)
                })
                used_users.update(cycle_users)
                total_value += value
            
            if len(selected_cycles) >= max_cycles:
                break
        
        return selected_cycles, total_value, len(used_users)
    
    def run_final_matching(self):
        """Ejecuta matching final"""
        print("="*70)
        print("ALGORITMO TREQE FINAL - EJECUCION")
        print("="*70)
        
        # Paso 1: Construir grafo
        print("\n1. Construyendo grafo de preferencias...")
        start_time = time.time()
        graph = self.build_preference_graph()
        graph_time = time.time() - start_time
        
        total_edges = sum(len(data.get('owners', set())) for data in graph.values())
        avg_out_degree = total_edges / self.n_users if self.n_users > 0 else 0
        
        print(f"   Usuarios: {self.n_users}")
        print(f"   Preferencias promedio: {self.avg_preferences}")
        print(f"   Aristas totales: {total_edges}")
        print(f"   Grado salida promedio: {avg_out_degree:.1f}")
        print(f"   Tiempo construccion: {graph_time:.3f}s")
        
        # Paso 2: Buscar ciclos
        print(f"\n2. Buscando ciclos (k=2 a {self.k_max})...")
        start_time = time.time()
        cycles_by_k = self.find_cycles_optimized(graph, k_values=list(range(2, self.k_max + 1)))
        cycle_time = time.time() - start_time
        
        print(f"   Tiempo busqueda: {cycle_time:.3f}s")
        for k in range(2, self.k_max + 1):
            cycles = cycles_by_k.get(k, [])
            print(f"   Ciclos k={k}: {len(cycles)}")
        
        # Paso 3: Selección greedy
        print("\n3. Seleccionando ciclos optimos (greedy)...")
        start_time = time.time()
        selected_cycles, total_value, users_matched = self.greedy_cycle_selection(cycles_by_k)
        selection_time = time.time() - start_time
        
        print(f"   Tiempo seleccion: {selection_time:.3f}s")
        print(f"   Ciclos seleccionados: {len(selected_cycles)}")
        print(f"   Usuarios emparejados: {users_matched}/{self.n_users}")
        print(f"   Cobertura: {users_matched/self.n_users*100:.1f}%")
        print(f"   Valor total intercambiado: EUR{total_value:.0f}")
        
        # Paso 4: Análisis por k
        print("\n4. ANALISIS POR TAMAÑO DE RUEDA:")
        print("   " + "-"*50)
        
        cycles_by_k_selected = defaultdict(list)
        value_by_k = defaultdict(float)
        users_by_k = defaultdict(set)
        
        for cycle_data in selected_cycles:
            k = cycle_data['k']
            cycles_by_k_selected[k].append(cycle_data)
            value_by_k[k] += cycle_data['value']
            users_by_k[k].update(cycle_data['users'])
        
        for k in sorted(cycles_by_k_selected.keys()):
            cycles = cycles_by_k_selected[k]
            value = value_by_k[k]
            users = len(users_by_k[k])
            
            print(f"\n   k={k}:")
            print(f"     Ciclos: {len(cycles)}")
            print(f"     Usuarios: {users}")
            print(f"     Valor total: EUR{value:.0f}")
            if cycles:
                print(f"     Valor por ciclo: EUR{value/len(cycles):.0f}")
            if users > 0:
                print(f"     Valor por usuario: EUR{value/users:.0f}")
        
        # Paso 5: Recomendaciones
        print("\n5. RECOMENDACIONES OPTIMIZADAS:")
        print("   " + "-"*50)
        
        best_k = None
        best_efficiency = -1
        
        for k in range(2, self.k_max + 1):
            if k in value_by_k and users_by_k[k]:
                efficiency = value_by_k[k] / len(users_by_k[k])
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_k = k
        
        if best_k:
            print(f"   k optimo: {best_k} (EUR{best_efficiency:.0f} por usuario)")
            
            if best_k == 2:
                print("   * Enfocar en intercambios directos 1:1")
                print("   * Simple, rapido, facil de entender")
            elif best_k == 3:
                print("   * Balance perfecto complejidad/valor")
                print("   * Resuelve matching asimetrico eficientemente")
            elif best_k >= 4:
                print("   * Alto valor por usuario")
                print("   * Requiere mas computo pero vale la pena")
        
        print(f"\n   Estrategia recomendada:")
        print(f"   1. Buscar ciclos k={best_k} primero (maximo valor/usuario)")
        print(f"   2. Luego k={best_k-1 if best_k>2 else 2} para usuarios restantes")
        print(f"   3. Finalmente k=2 para casos dificiles")
        
        total_time = graph_time + cycle_time + selection_time
        print(f"\n   Performance:")
        print(f"   * Tiempo total: {total_time:.3f}s")
        if total_time > 0:
            print(f"   * Usuarios por segundo: {self.n_users/total_time:.0f}")
            print(f"   * Valor por segundo: EUR{total_value/total_time:.0f}")
        
        # Resumen ejecutivo
        print("\n" + "="*70)
        print("RESUMEN EJECUTIVO - TREQE OPTIMIZADO")
        print("="*70)
        
        print(f"\n* Usuarios totales: {self.n_users}")
        print(f"* Usuarios emparejados: {users_matched} ({users_matched/self.n_users*100:.1f}%)")
        print(f"* Valor intercambiado: EUR{total_value:.0f}")
        if users_matched > 0:
            print(f"* Valor por usuario: EUR{total_value/users_matched:.0f}")
        print(f"* Tiempo ejecucion: {total_time:.3f}s")
        print(f"* k optimo identificado: {best_k}")
        
        print(f"\nVIABILIDAD CONFIRMADA:")
        coverage_ok = users_matched/self.n_users >= 0.5
        value_ok = total_value/users_matched >= 100 if users_matched > 0 else False
        time_ok = total_time < 5
        
        print(f"   * Cobertura >50%: {'OK' if coverage_ok else 'NO'}")
        print(f"   * Valor/usuario >EUR100: {'OK' if value_ok else 'NO'}")
        print(f"   * Tiempo <5s: {'OK' if time_ok else 'NO'}")
        
        if coverage_ok and value_ok and time_ok:
            print("\n[OK] ALGORITMO OPTIMIZADO - LISTO PARA PRODUCCION")
        else:
            print("\n[ALERTA] ALGORITMO NECESITA OPTIMIZACION")
        
        return {
            'n_users': self.n_users,
            'users_matched': users_matched,
            'coverage': users_matched / self.n_users,
            'total_value': total_value,
            'value_per_user': total_value / users_matched if users_matched > 0 else 0,
            'total_time': total_time,
            'best_k': best_k,
            'selected_cycles': selected_cycles,
            'cycles_by_k': {k: len(cycles) for k, cycles in cycles_by_k.items()}
        }

def main():
    """Función principal"""
    print("ALGORITMO TREQE FINAL - VERSION OPTIMIZADA")
    print("k>2 RESUELVE matching asimetrico")
    print("="*70)
    
    # Ejecutar algoritmo
    algorithm = TreqeFinalAlgorithm(n_users=100, avg_preferences=3, k_max=4)
    result = algorithm.run_final_matching()
    
    # Mostrar ejemplos
    print("\n" + "="*70)
    print("EJEMPLOS DE CICLOS ENCONTRADOS:")
    print("="*70)
    
    selected = result['selected_cycles']
    for i, cycle_data in enumerate(selected[:5]):
        cycle = cycle_data['cycle']
        k = cycle_data['k']
        value = cycle_data['value']
        print(f"Ciclo {i+1} (k={k}, EUR{value:.0f}): {cycle}")
        
        # Mostrar items intercambiados
        print("  Intercambio:")
        for j in range(k):
            user_from = cycle[j]
            user_to = cycle[(j + 1) % k]
            item_from = algorithm.users[user_from]['offered']['item']
            item_to = algorithm.users[user_to]['offered']['item']
            print(f"    Usuario {user_from} -> Usuario {user_to}: {item_from}")
    
    print("\n" + "="*70)
    print("CONCLUSION FINAL:")
    print("="*70)
    
    print("\n1. k={} es OPTIMO para Treqe".format(result['best_k']))
    print("2. Cobertura: {:.1f}% usuarios emparejados".format(result['coverage']*100))
    print("3. Valor por usuario: EUR{:.0f}".format(result['value_per_user']))
    print("4. Tiempo ejecucion: {:.3f}s".format(result['total_time']))
    
    print("\nRECOMENDACION DE IMPLEMENTACION:")
    print("-"*40)
    print("1. Implementar algoritmo greedy con k_max={}".format(result['best_k']))
    print("2. Ejecutar cada 10 minutos (batch processing)")
    print("3. Cachear resultados 24h")
    print("4. Monitorear cobertura real y ajustar k_max")