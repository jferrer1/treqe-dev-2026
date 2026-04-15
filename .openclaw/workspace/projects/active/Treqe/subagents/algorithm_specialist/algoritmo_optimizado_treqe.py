#!/usr/bin/env python3
"""
ALGORITMO OPTIMIZADO PARA RUEDAS DE INTERCAMBIO TREQE
Versión optimizada para manejar k=4-6 usuarios con heurísticas y aproximaciones
"""

import json
import random
import time
import math
import heapq
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque

print("="*80)
print("ALGORITMO OPTIMIZADO TREQE - RUEDAS k=4-6")
print("="*80)

# ========== ESTRUCTURAS DE DATOS OPTIMIZADAS ==========

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
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.id == other.id

@dataclass 
class User:
    id: str
    name: str
    level: UserLevel
    reputation: float  # 0-1000
    offered_items: List[Item]
    desired_items: List[Item]
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id
    
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

# ========== ALGORITMOS DE APROXIMACIÓN ==========

class OptimizedTreqeMatching:
    """Algoritmos optimizados para ruedas grandes (k=4-6)"""
    
    def __init__(self, users: List[User]):
        self.users = users
        self.user_dict = {u.id: u for u in users}
        
        # Precomputar estructuras para optimización
        self.item_to_users = defaultdict(set)  # item → usuarios que lo ofrecen
        self.user_desires = defaultdict(set)   # usuario → items deseados
        self.category_users = defaultdict(set) # categoría → usuarios con items
        
        for user in users:
            for item in user.offered_items:
                self.item_to_users[item.id].add(user.id)
                self.category_users[item.category].add(user.id)
            for item in user.desired_items:
                self.user_desires[user.id].add(item.id)
    
    def greedy_cycle_finding(self, max_k: int = 6, time_limit: float = 5.0) -> List[Dict]:
        """
        Heurística greedy para encontrar ciclos de hasta max_k usuarios
        Basado en algoritmo de inserción (cheapest insertion)
        """
        print(f"\n[1] GREEDY CYCLE FINDING (k ≤ {max_k})")
        print(f"    Time limit: {time_limit}s")
        
        start_time = time.time()
        all_matches = []
        matched_users = set()
        matched_items = set()
        
        # Primero buscar ciclos pequeños (k=2-3) exactos
        small_cycles = self.find_small_cycles_exact(max_k=3)
        for cycle in small_cycles:
            all_matches.append(cycle)
            matched_users.update(cycle["participants"])
            for exchange in cycle["exchanges"]:
                matched_items.add(exchange["item"])
        
        # Usuarios no emparejados
        remaining_users = [u for u in self.users if u.id not in matched_users]
        
        if not remaining_users or max_k <= 3:
            return all_matches
        
        # Para k=4+, usar heurística greedy
        print(f"    Users remaining for k=4+ search: {len(remaining_users)}")
        
        # Agrupar usuarios por categorías similares
        user_groups = self.cluster_users_by_preferences(remaining_users)
        
        for group in user_groups:
            if time.time() - start_time > time_limit:
                print(f"    Time limit reached ({time_limit}s)")
                break
            
            if len(group) >= 4:
                # Intentar encontrar ciclo en este grupo
                cycle = self.find_cycle_in_group_greedy(group, max_k)
                if cycle:
                    all_matches.append(cycle)
        
        elapsed = time.time() - start_time
        print(f"    Execution time: {elapsed:.3f}s")
        print(f"    Total matches found: {len(all_matches)}")
        
        return all_matches
    
    def find_small_cycles_exact(self, max_k: int = 3) -> List[Dict]:
        """Búsqueda exacta para ciclos pequeños (k ≤ 3)"""
        cycles = []
        
        if max_k >= 2:
            cycles.extend(self.find_direct_matches())
        
        if max_k >= 3:
            cycles.extend(self.find_3_cycles_exact())
        
        return cycles
    
    def find_direct_matches(self) -> List[Dict]:
        """Encuentra matches directos 1:1 (k=2)"""
        matches = []
        matched = set()
        
        for i, u1 in enumerate(self.users):
            if u1.id in matched:
                continue
                
            for u2 in self.users[i+1:]:
                if u2.id in matched:
                    continue
                
                # Buscar items que coincidan
                for item1 in u1.offered_items:
                    for item2 in u2.offered_items:
                        if (item1.id in self.user_desires[u2.id] and 
                            item2.id in self.user_desires[u1.id]):
                            
                            match = self.create_direct_match(u1, u2, item1, item2)
                            matches.append(match)
                            matched.add(u1.id)
                            matched.add(u2.id)
                            break
                    if u1.id in matched:
                        break
                if u1.id in matched:
                    break
        
        return matches
    
    def find_3_cycles_exact(self) -> List[Dict]:
        """Búsqueda exacta de ciclos de 3 usuarios"""
        cycles = []
        n = len(self.users)
        
        # Búsqueda optimizada con pruning
        for i in range(n):
            u1 = self.users[i]
            
            for j in range(i+1, n):
                u2 = self.users[j]
                
                # Pruning: solo continuar si hay alguna conexión potencial
                if not self.potential_connection(u1, u2):
                    continue
                
                for k in range(j+1, n):
                    u3 = self.users[k]
                    
                    # Verificar ciclo A→B→C→A
                    cycle_found = False
                    cycle_items = []
                    
                    # Buscar combinación que forme ciclo
                    for item1 in u1.offered_items:
                        if item1.id not in self.user_desires[u2.id]:
                            continue
                            
                        for item2 in u2.offered_items:
                            if item2.id not in self.user_desires[u3.id]:
                                continue
                                
                            for item3 in u3.offered_items:
                                if item3.id not in self.user_desires[u1.id]:
                                    continue
                                
                                # Ciclo encontrado
                                cycle_found = True
                                cycle_items = [(u1, item1, u2, item2),
                                             (u2, item2, u3, item3),
                                             (u3, item3, u1, item1)]
                                break
                            
                            if cycle_found:
                                break
                        
                        if cycle_found:
                            break
                    
                    if cycle_found:
                        cycle = self.create_cycle_match(cycle_items, "circular")
                        cycles.append(cycle)
        
        return cycles
    
    def cluster_users_by_preferences(self, users: List[User]) -> List[List[User]]:
        """Agrupa usuarios por preferencias similares"""
        # Agrupar por categorías de items ofrecidos/deseados
        category_groups = defaultdict(list)
        
        for user in users:
            # Determinar categorías principales del usuario
            offered_cats = set(item.category for item in user.offered_items)
            desired_cats = set(item.category for item in user.desired_items)
            user_cats = offered_cats.union(desired_cats)
            
            # Asignar a grupo basado en categorías
            if user_cats:
                primary_cat = max(user_cats, key=lambda c: len([i for i in user.offered_items if i.category == c]))
                category_groups[primary_cat].append(user)
            else:
                category_groups["other"].append(user)
        
        # Limitar tamaño de grupos para eficiencia
        max_group_size = 20
        groups = []
        for cat, user_list in category_groups.items():
            if len(user_list) > max_group_size:
                # Dividir grupo grande
                for i in range(0, len(user_list), max_group_size):
                    groups.append(user_list[i:i+max_group_size])
            else:
                groups.append(user_list)
        
        return groups
    
    def find_cycle_in_group_greedy(self, group: List[User], max_k: int) -> Optional[Dict]:
        """
        Heurística greedy para encontrar ciclo en grupo pequeño
        Basado en algoritmo de nearest neighbor
        """
        if len(group) < 4:
            return None
        
        # Intentar construir ciclo empezando por cada usuario
        for start_user in group[:5]:  # Limitar intentos
            cycle = self.build_cycle_greedy(start_user, group, max_k)
            if cycle:
                return cycle
        
        return None
    
    def build_cycle_greedy(self, start_user: User, group: List[User], max_k: int) -> Optional[Dict]:
        """Construye ciclo greedy empezando por start_user"""
        visited = {start_user.id}
        path = [start_user]
        exchanges = []
        
        current_user = start_user
        
        while len(path) < max_k:
            # Encontrar mejor siguiente usuario
            next_user = None
            best_item = None
            best_score = -1
            
            for candidate in group:
                if candidate.id in visited:
                    continue
                
                # Buscar item que current_user ofrezca y candidate desee
                for item in current_user.offered_items:
                    if item.id in self.user_desires[candidate.id]:
                        # Calcular score basado en valor y reputación
                        score = item.value * current_user.reputation_multiplier()
                        
                        if score > best_score:
                            best_score = score
                            next_user = candidate
                            best_item = item
                            break
            
            if not next_user:
                # No se puede continuar el ciclo
                break
            
            # Añadir al ciclo
            exchanges.append((current_user, best_item, next_user))
            visited.add(next_user.id)
            path.append(next_user)
            current_user = next_user
        
        # Intentar cerrar el ciclo (último → primero)
        if len(path) >= 3:
            last_user = path[-1]
            
            # Buscar item que last_user ofrezca y start_user desee
            for item in last_user.offered_items:
                if item.id in self.user_desires[start_user.id]:
                    exchanges.append((last_user, item, start_user))
                    
                    # Crear match
                    cycle_items = []
                    for from_user, item, to_user in exchanges:
                        cycle_items.append((from_user, item, to_user, None))  # to_item se calcula después
                    
                    return self.create_cycle_match_greedy(cycle_items, path)
        
        return None
    
    def potential_connection(self, u1: User, u2: User) -> bool:
        """Verifica si hay conexión potencial entre dos usuarios"""
        # Verificar si u1 ofrece algo que u2 desea
        for item in u1.offered_items:
            if item.id in self.user_desires[u2.id]:
                return True
        
        # Verificar si u2 ofrece algo que u1 desea
        for item in u2.offered_items:
            if item.id in self.user_desires[u1.id]:
                return True
        
        return False
    
    def create_direct_match(self, u1: User, u2: User, item1: Item, item2: Item) -> Dict:
        """Crea estructura de match directo"""
        value_diff = item2.value - item1.value
        
        if value_diff > 0:
            compensation = value_diff * (1 - u1.commission_rate()) * u1.reputation_multiplier()
            payment = value_diff * (1 + u2.commission_rate()) / u2.reputation_multiplier()
        else:
            compensation = abs(value_diff) * (1 - u2.commission_rate()) * u2.reputation_multiplier()
            payment = abs(value_diff) * (1 + u1.commission_rate()) / u1.reputation_multiplier()
        
        return {
            "type": "direct",
            "participants": [u1.id, u2.id],
            "exchanges": [
                {"from": u1.id, "to": u2.id, "item": item1.id, "value": item1.value},
                {"from": u2.id, "to": u1.id, "item": item2.id, "value": item2.value}
            ],
            "compensations": {
                u1.id: compensation if value_diff > 0 else -payment,
                u2.id: -payment if value_diff > 0 else compensation
            },
            "total_value": (item1.value + item2.value) / 2,
            "size": 2
        }
    
    def create_cycle_match(self, cycle_items: List[Tuple], cycle_type: str) -> Dict:
        """Crea estructura de match circular"""
        participants = set()
        exchanges = []
        total_value = 0
        
        for from_user, from_item, to_user, to_item in cycle_items:
            participants.add(from_user.id)
            participants.add(to_user.id)
            
            exchanges.append({
                "from": from_user.id,
                "to": to_user.id,
                "item": from_item.id,
                "value": from_item.value
            })
            
            total_value += from_item.value
        
        # Calcular compensaciones (simplificado)
        compensations = {}
        avg_value = total_value / len(cycle_items)
        
        for user_id in participants:
            user = self.user_dict[user_id]
            # Compensación basada en diferencia con valor promedio
            compensations[user_id] = avg_value * 0.1 * user.reputation_multiplier()
        
        return {
            "type": cycle_type,
            "participants": list(participants),
            "exchanges": exchanges,
            "compensations": compensations,
            "total_value": total_value / len(cycle_items),
            "size": len(participants)
        }
    
    def create_cycle_match_greedy(self, cycle_items: List[Tuple], path: List[User]) -> Dict:
        """Crea match para ciclo greedy"""
        exchanges = []
        total_value = 0
        
        for i, (from_user, item, to_user, _) in enumerate(cycle_items):
            exchanges.append({
                "from": from_user.id,
                "to": to_user.id,
                "item": item.id,
                "value": item.value
            })
            total_value += item.value
        
        # Compensaciones simplificadas
        compensations = {}
        for user in path:
            compensations[user.id] = 0.0  # Placeholder
        
        return {
            "type": "greedy_circular",
            "participants": [u.id for u in path],
            "exchanges": exchanges,
            "compensations": compensations,
            "total_value": total_value / len(path),
            "size": len(path)
        }

# ========== ALGORITMO GENÉTICO PARA OPTIMIZACIÓN ==========

class GeneticCycleOptimizer:
    """Algoritmo genético para optimizar ciclos grandes"""
    
    def __init__(self, users: List[User], population_size: int = 50, generations: int = 100):
        self.users = users
        self.population_size = population_size
        self.generations = generations
        self.user_dict = {u.id: u for u in users}
    
    def optimize(self, cycle_size: int = 4) -> List[Dict]:
        """Ejecuta algoritmo genético para encontrar buenos ciclos"""
        print(f"\n[2] GENETIC ALGORITHM OPTIMIZATION (k={cycle_size})")
        
        # Inicializar población
        population = self.initialize_population(cycle_size)
        
        best_cycle = None
        best_fitness = -float('inf')
        
        for gen in range(self.generations):
            # Evaluar fitness
            fitness_scores = []
            for cycle in population:
                fitness = self.calculate_fitness(cycle)
                fitness_scores.append((fitness, cycle))
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_cycle = cycle
            
            # Selección
            selected = self.selection(fitness_scores)
            
            # Cruzamiento (crossover)
            new_population = self.crossover(selected, cycle_size)
            
            # Mutación
            population = self.mutation(new_population)
            
            if gen % 20 == 0:
                print(f"    Generation {gen}: best fitness = {best_fitness:.2f}")
        
        if best