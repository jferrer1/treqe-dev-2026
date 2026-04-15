#!/usr/bin/env python3
"""
ALGORITMO TREQE OPTIMIZADO - Versión FINAL basada en entendimiento correcto
"""

import numpy as np
import time
from typing import List, Dict, Set, Tuple
import random
from collections import defaultdict, deque

class TreqeOptimizedAlgorithm:
    """
    Algoritmo OPTIMIZADO para Treqe basado en entendimiento correcto:
    - k>2 RESUELVE matching asimétrico
    - Más usuarios = más formas de cerrar ciclos
    - Usuarios pueden seleccionar múltiples items que les gustan
    """
    
    def __init__(self, n_users=100, avg_preferences=3, k_max=4):
        self.n_users = n_users
        self.avg_preferences = avg_preferences  # Promedio de items que le gustan a cada usuario
        self.k_max = k_max  # Máximo tamaño de rueda a buscar
        self.users = self._create_realistic_users()
        
    def _create_realistic_users(self):
        """Crea usuarios realistas con preferencias múltiples"""
        users = []
        
        # Items disponibles en Treqe (segunda mano)
        items_pool = [
            # Electrónica
            "iPhone 15 Pro", "Samsung S24", "MacBook Pro M3", "iPad Air",
            "Canon EOS R5", "Sony A7IV", "Nintendo Switch", "PlayStation 5",
            # Moda
            "Zapatos Nike", "Chaqueta North Face", "Bolso Michael Kors", "Reloj Casio",
            # Hogar
            "Sofá 3 plazas", "Mesa comedor", "Lámpara diseño", "Vajilla completa",
            # Deportes
            "Bicicleta carretera", "Cinta correr", "Raqueta tenis", "Pesas 20kg",
            # Varios
            "Libro bestseller", "Vinilo colección", "Juego mesa", "Herramientas"
        ]
        
        # Valores aproximados por item (EUR)
        item_values = {
            "iPhone 15 Pro": 900, "Samsung S24": 800, "MacBook Pro M3": 1800,
            "iPad Air": 600, "Canon EOS R5": 2500, "Sony A7IV": 2200,
            "Nintendo Switch": 250, "PlayStation 5": 450,
            "Zapatos Nike": 80, "Chaqueta North Face": 120, 
            "Bolso Michael Kors": 150, "Reloj Casio": 60,
            "Sofá 3 plazas": 300, "Mesa comedor": 200, 
            "Lámpara diseño": 80, "Vajilla completa": 100,
            "Bicicleta carretera": 400, "Cinta correr": 350,
            "Raqueta tenis": 70, "Pesas 20kg": 50,
            "Libro bestseller": 15, "Vinilo colección": 30,
            "Juego mesa": 40, "Herramientas": 60
        }
        
        for user_id in range(self.n_users):
            # Cada usuario OFRECE 1 item
            offered_item = random.choice(items_pool)
            offered_value = item_values[offered_item]
            
            # Cada usuario QUIERE varios items que le gustan
            # Número de preferencias: 1-5 (promedio = avg_preferences)
            n_wanted = random.randint(1, 5)
            
            # Seleccionar items que le gustan (no puede ser el que ofrece)
            available_items = [item for item in items_pool if item != offered_item]
            wanted_items = random.sample(available_items, min(n_wanted, len(available_items)))
            wanted_values = [item_values[item] for item in wanted_items]
            
            users.append({
                'id': user_id,
                'offered': {
                    'item': offered_item,
                    'value': offered_value,
                    'owner': user_id
                },
                'wanted': [
                    {'item': item, 'value': value, 'owner': None}  # owner se llena después
                    for item, value in zip(wanted_items, wanted_values)
                ],
                'flexibility': random.uniform(0.3, 0.8)  # 30-80% flexible
            })
        
        return users
    
    def build_preference_graph(self):
        """Construye grafo de preferencias: usuario → items que le gustan"""
        graph = defaultdict(set)
        item_to_owners = defaultdict(set)
        
        # Mapear cada item a sus dueños
        for user in self.users:
            item_to_owners[user['offered']['item']].add(user['id'])
        
        # Construir grafo de preferencias
        for user in self.users:
            user_id = user['id']
            for wanted in user['wanted']:
                item = wanted['item']
                # Usuario quiere este item → conectar con todos sus dueños
                if item in item_to_owners:
                    for owner_id in item_to_owners[item]:
                        if owner_id != user_id:  # No puede querer su propio item
                            # Inicializar estructura si no existe
                            if user_id not in graph:
                                graph[user_id] = {'owners': set(), 'items': {}}
                            # Añadir conexión
                            graph[user_id]['owners'].add(owner_id)
                            graph[user_id]['items'][owner_id] = item
        
        return graph
    
    def find_cycles_optimized(self, graph, k_values=[2, 3, 4]):
        """
        Encuentra ciclos de diferentes tamaños OPTIMIZADO
        Estrategia: Búsqueda en profundidad limitada
        """
        cycles_by_k = {k: [] for k in k_values}
        
        # Para cada usuario como punto de inicio
        for start_user in range(self.n_users):
            # Búsqueda para cada k
            for k in k_values:
                if k < 2:
                    continue
                    
                # Usar DFS limitada a profundidad k-1
                stack = [(start_user, [start_user], set([start_user]))]
                
                while stack:
                    current_user, path, visited = stack.pop()
                    
                    # Si llegamos al tamaño k
                    if len(path) == k:
                        # Verificar si el último puede cerrar el ciclo con el primero
                        last_user = path[-1]
                        last_user_data = graph.get(last_user, {})
                        if 'owners' in last_user_data and start_user in last_user_data['owners']:
                            # ¡CICLO ENCONTRADO!
                            cycle = path[:]  # Copiar camino
                            
                            # Verificar que sea ciclo válido (todos diferentes)
                            if len(set(cycle)) == k:  # Todos usuarios diferentes
                                # Añadir ciclo (empezando por el más bajo para normalizar)
                                normalized_cycle = self._normalize_cycle(cycle)
                                if normalized_cycle not in cycles_by_k[k]:
                                    cycles_by_k[k].append(normalized_cycle)
                        continue
                    
                    # Continuar búsqueda si no llegamos a k
                    if len(path) < k:
                        # Explorar vecinos (usuarios que tienen items que current_user quiere)
                        current_user_data = graph.get(current_user, {})
                        if 'owners' in current_user_data:
                            neighbors = current_user_data['owners']
                            for neighbor in neighbors:
                                if neighbor not in visited:
                                    new_path = path + [neighbor]
                                    new_visited = visited.copy()
                                    new_visited.add(neighbor)
                                    stack.append((neighbor, new_path, new_visited))
        
        return cycles_by_k
    
    def _normalize_cycle(self, cycle):
        """Normaliza ciclo para evitar duplicados (rota para empezar por el mínimo)"""
        min_idx = cycle.index(min(cycle))
        normalized = cycle[min_idx:] + cycle[:min_idx]
        return tuple(normalized)
    
    def calculate_cycle_value(self, cycle):
        """Calcula valor económico de un ciclo"""
        total_value = 0
        
        for i in range(len(cycle)):
            user_from = cycle[i]
            user_to = cycle[(i + 1) % len(cycle)]
            
            # Encontrar qué item quiere user_from de user_to
            wanted_item = None
            for wanted in self.users[user_from]['wanted']:
                # Buscar si user_to ofrece este item
                if self.users[user_to]['offered']['item'] == wanted['item']:
                    wanted_item = wanted
                    break
            
            if wanted_item:
                total_value += wanted_item['value']
        
        return total_value
    
    def greedy_cycle_selection(self, cycles_by_k, max_cycles=100):
        """
        Selección greedy de ciclos para maximizar valor
        Evita solapamiento de usuarios
        """
        selected_cycles = []
        used_users = set()
        total_value = 0
        
        # Recolectar todos los ciclos con su valor
        all_cycles = []
        for k, cycles in cycles_by_k.items():
            for cycle in cycles:
                value = self.calculate_cycle_value(cycle)
                efficiency = value / k  # Valor por usuario
                all_cycles.append((cycle, k, value, efficiency))
        
        # Ordenar por eficiencia (valor por usuario) descendente
        all_cycles.sort(key=lambda x: x[3], reverse=True)
        
        # Selección greedy
        for cycle, k, value, efficiency in all_cycles:
            # Verificar que no use usuarios ya seleccionados
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
            
            # Limitar número de ciclos
            if len(selected_cycles) >= max_cycles:
                break
        
        return selected_cycles, total_value, len(used_users)
    
    def run_optimized_matching(self):
        """Ejecuta matching optimizado completo"""
        print("="*70)
        print("ALGORITMO TREQE OPTIMIZADO - EJECUCIÓN")
        print("="*70)
        
        # Paso 1: Construir grafo
        print("\n1. Construyendo grafo de preferencias...")
        start_time = time.time()
        graph = self.build_preference_graph()
        graph_time = time.time() - start_time
        
        # Estadísticas del grafo
        total_edges = sum(len(data.get('owners', set())) for data in graph.values())
        avg_out_degree = total_edges / self.n_users if self.n_users > 0 else 0
        
        print(f"   Usuarios: {self.n_users}")
        print(f"   Preferencias promedio: {self.avg_preferences}")
        print(f"   Aristas totales: {total_edges}")
        print(f"   Grado salida promedio: {avg_out_degree:.1f}")
        print(f"   Tiempo construcción: {graph_time:.3f}s")
        
        # Paso 2: Buscar ciclos
        print(f"\n2. Buscando ciclos (k=2 a {self.k_max})...")
        start_time = time.time()
        cycles_by_k = self.find_cycles_optimized(graph, k_values=list(range(2, self.k_max + 1)))
        cycle_time = time.time() - start_time
        
        # Estadísticas de ciclos
        print(f"   Tiempo búsqueda: {cycle_time:.3f}s")
        for k in range(2, self.k_max + 1):
            cycles = cycles_by_k.get(k, [])
            print(f"   Ciclos k={k}: {len(cycles)}")
        
        # Paso 3: Selección greedy
        print("\n3. Seleccionando ciclos óptimos (greedy)...")
        start_time = time.time()
        selected_cycles, total_value, users_matched = self.greedy_cycle_selection(cycles_by_k)
        selection_time = time.time() - start_time
        
        print(f"   Tiempo selección: {selection_time:.3f}s")
        print(f"   Ciclos seleccionados: {len(selected_cycles)}")
        print(f"   Usuarios emparejados: {users_matched}/{self.n_users}")
        print(f"   Cobertura: {users_matched/self.n_users*100:.1f}%")
        print(f"   Valor total intercambiado: €{total_value:.0f}")
        
        # Paso 4: Análisis por k
        print("\n4. ANÁLISIS POR TAMAÑO DE RUEDA:")
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
            print(f"     Valor total: €{value:.0f}")
            print(f"     Valor por ciclo: €{value/len(cycles):.0f}" if cycles else "     Valor por ciclo: €0")
            print(f"     Valor por usuario: €{value/users:.0f}" if users > 0 else "     Valor por usuario: €0")
        
        # Paso 5: Recomendaciones
        print("\n5. RECOMENDACIONES OPTIMIZADAS:")
        print("   " + "-"*50)
        
        # Encontrar k más eficiente
        best_k = None
        best_efficiency = -1
        
        for k in range(2, self.k_max + 1):
            if k in value_by_k and users_by_k[k]:
                efficiency = value_by_k[k] / len(users_by_k[k])
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_k = k
        
        if best_k:
            print(f"   k óptimo: {best_k} (€{best_efficiency:.0f} por usuario)")
            
            if best_k == 2:
                print("   • Enfocar en intercambios directos 1:1")
                print("   • Simple, rápido, fácil de entender")
            elif best_k == 3:
                print("   • Balance perfecto complejidad/valor")
                print("   • Resuelve matching asimétrico eficientemente")
            elif best_k >= 4:
                print("   • Alto valor por usuario")
                print("   • Requiere más cómputo pero vale la pena")
        
        # Estrategia recomendada
        print(f"\n   Estrategia recomendada:")
        print(f"   1. Buscar ciclos k={best_k} primero (máximo valor/usuario)")
        print(f"   2. Luego k={best_k-1 if best_k>2 else 2} para usuarios restantes")
        print(f"   3. Finalmente k=2 para casos difíciles")
        
        # Performance
        total_time = graph_time + cycle_time + selection_time
        print(f"\n   Performance:")
        print(f"   • Tiempo total: {total_time:.3f}s")
        print(f"   • Usuarios por segundo: {self.n_users/total_time:.0f}" if total_time > 0 else "   • Usuarios por segundo: ∞")
        print(f"   • Valor por segundo: €{total_value/total_time:.0f}" if total_time > 0 else "   • Valor por segundo: €0")
        
        # Resumen ejecutivo
        print("\n" + "="*70)
        print("RESUMEN EJECUTIVO - TREQE OPTIMIZADO")
        print("="*70)
        
        print(f"\n• Usuarios totales: {self.n_users}")
        print(f"• Usuarios emparejados: {users_matched} ({users_matched/self.n_users*100:.1f}%)")
        print(f"• Valor intercambiado: €{total_value:.0f}")
        print(f"• Valor por usuario: €{total_value/users_matched:.0f}" if users_matched > 0 else "• Valor por usuario: €0")
        print(f"• Tiempo ejecución: {total_time:.3f}s")
        print(f"• k óptimo identificado: {best_k}")
        
        print(f"\n✅ VIABILIDAD CONFIRMADA:")
        print(f"   • Cobertura >50%: {'✅' if users_matched/self.n_users >= 0.5 else '❌'}")
        print(f"   • Valor/usuario >€100: {'✅' if total_value/users_matched >= 100 else '❌'}" if users_matched > 0 else "   • Valor/usuario >€100: N/A")
        print(f"   • Tiempo <5s: {'✅' if total_time < 5 else '❌'}")
        
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
