#!/usr/bin/env python3
"""
ALGORITMO TREQE CORREGIDO - Lógica económica correcta
Implementa compensaciones realistas: quien recibe item de mayor valor PAGA diferencia
"""

import time
import random
import math
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict, deque
import heapq

class TreqeUser:
    """Usuario de Treqe con lógica económica correcta"""
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
        self.reputation = 50  # Puntuación inicial
        
    def __repr__(self):
        return f"User({self.id}, offers:{self.offered['item']}€{self.offered['value']}, wants:{len(self.wanted)} items)"

class TreqeCycle:
    """Ciclo de intercambio con compensaciones correctas"""
    def __init__(self, user_ids: List[int], users: List[TreqeUser]):
        self.user_ids = user_ids
        self.k = len(user_ids)
        self.users = {user.id: user for user in users}
        self.calculate_compensations()
    
    def calculate_compensations(self):
        """Calcular compensaciones según lógica económica CORRECTA"""
        self.exchanges = []
        self.compensations = {}
        self.total_value_exchanged = 0
        
        # Determinar qué recibe cada usuario
        for i in range(self.k):
            user_from_id = self.user_ids[i]
            user_to_id = self.user_ids[(i + 1) % self.k]
            
            user_from = self.users[user_from_id]
            user_to = self.users[user_to_id]
            
            # Encontrar qué item quiere user_from de user_to
            item_received = None
            item_value = 0
            
            for wanted in user_from.wanted:
                if user_to.offered['item'] == wanted['item']:
                    item_received = wanted['item']
                    item_value = wanted['value']
                    break
            
            if item_received:
                self.exchanges.append({
                    'from': user_from_id,
                    'to': user_to_id,
                    'gives': user_from.offered['item'],
                    'gives_value': user_from.offered['value'],
                    'receives': item_received,
                    'receives_value': item_value
                })
                
                self.total_value_exchanged += item_value
        
        # Calcular compensaciones: quien recibe item de MAYOR valor PAGA diferencia
        for exchange in self.exchanges:
            user_id = exchange['from']
            gives_value = exchange['gives_value']
            receives_value = exchange['receives_value']
            
            # Diferencia: positivo si recibe más valor (debe PAGAR), negativo si da más valor (recibe)
            difference = receives_value - gives_value
            
            # Aplicar comisión Treqe (4-8% según reputación)
            user = self.users[user_id]
            commission_rate = 0.08 if user.reputation < 60 else 0.06 if user.reputation < 80 else 0.04
            commission = abs(difference) * commission_rate
            
            if difference > 0:
                # Recibe item de MAYOR valor → PAGA diferencia + comisión
                payment = difference + commission
                self.compensations[user_id] = {
                    'type': 'pays',
                    'amount': payment,
                    'reason': f"Recibe {exchange['receives']} (€{receives_value}) que vale €{difference} más que su {exchange['gives']} (€{gives_value})",
                    'commission': commission
                }
            elif difference < 0:
                # Da item de MAYOR valor → RECIBE diferencia - comisión
                receipt = abs(difference) - commission
                self.compensations[user_id] = {
                    'type': 'receives',
                    'amount': receipt,
                    'reason': f"Da {exchange['gives']} (€{gives_value}) que vale €{abs(difference)} más que lo que recibe {exchange['receives']} (€{receives_value})",
                    'commission': commission
                }
            else:
                # Valores iguales
                self.compensations[user_id] = {
                    'type': 'even',
                    'amount': 0,
                    'reason': f"Intercambio equitativo: {exchange['gives']} (€{gives_value}) por {exchange['receives']} (€{receives_value})",
                    'commission': 0
                }
    
    def get_user_proposal(self, user_id: int) -> Dict[str, Any]:
        """Generar propuesta para mostrar en la app a un usuario específico"""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        compensation = self.compensations.get(user_id, {'type': 'even', 'amount': 0})
        
        # Encontrar el intercambio de este usuario
        user_exchange = None
        for exchange in self.exchanges:
            if exchange['from'] == user_id:
                user_exchange = exchange
                break
        
        if not user_exchange:
            return None
        
        # Crear propuesta según lógica correcta
        if compensation['type'] == 'pays':
            proposal = {
                'title': f"Intercambio encontrado: Consigues {user_exchange['receives']}",
                'summary': f"Cambias {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial': f"Pagas €{compensation['amount']:.2f} (€{user_exchange['receives_value'] - user_exchange['gives_value']:.2f} diferencia + €{compensation['commission']:.2f} comisión)",
                'benefits': [
                    f"Obtienes EXACTAMENTE {user_exchange['receives']} que querías",
                    f"Sin buscar vendedor ni gestionar envíos por separado",
                    f"Garantía Treqe 30 días",
                    f"Mismo costo que vender {user_exchange['gives']} + comprar {user_exchange['receives']}, pero más simple"
                ],
                'action': "ACEPTAR POR CONVENIENCIA",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor, pagas €{compensation['amount']} = NETO: €{user_exchange['gives_value']} (EMPATE económico, ganas conveniencia)"
            }
        elif compensation['type'] == 'receives':
            proposal = {
                'title': f"Intercambio encontrado: Cambias {user_exchange['gives']} por {user_exchange['receives']} + €{compensation['amount']:.2f}",
                'summary': f"Cambias {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial': f"Recibes €{compensation['amount']:.2f} (€{abs(user_exchange['receives_value'] - user_exchange['gives_value']):.2f} diferencia - €{compensation['commission']:.2f} comisión)",
                'benefits': [
                    f"Obtienes {user_exchange['receives']} que querías",
                    f"Recibes €{compensation['amount']:.2f} en efectivo",
                    f"Todo gestionado en un solo intercambio",
                    f"Sin tener que vender {user_exchange['gives']} primero"
                ],
                'action': "ACEPTAR Y RECIBIR DINERO",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor + €{compensation['amount']} = NETO: €{user_exchange['gives_value']} (EMPATE económico, ganas conveniencia)"
            }
        else:
            proposal = {
                'title': f"Intercambio perfecto: Cambias {user_exchange['gives']} por {user_exchange['receives']}",
                'summary': f"Intercambio equitativo: {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial': "Sin ajuste monetario (valores iguales)",
                'benefits': [
                    f"Obtienes EXACTAMENTE lo que querías",
                    f"Intercambio perfectamente equilibrado",
                    f"Sin pagos adicionales",
                    f"Todo gestionado por Treqe"
                ],
                'action': "ACEPTAR INTERCAMBIO",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor = NETO: €{user_exchange['gives_value']} (EMPATE económico, ganas conveniencia)"
            }
        
        # Añadir información sobre otros participantes (anonimizada)
        other_users = []
        for exchange in self.exchanges:
            if exchange['from'] != user_id:
                other_users.append(f"Usuario intercambia {exchange['gives']} por {exchange['receives']}")
        
        proposal['other_participants'] = other_users
        proposal['total_participants'] = self.k
        proposal['treqe_commission_total'] = sum(ex['commission'] for ex in self.compensations.values() if isinstance(ex, dict) and 'commission' in ex)
        
        return proposal
    
    def __repr__(self):
        return f"Cycle(k={self.k}, users={self.user_ids}, value=€{self.total_value_exchanged:.0f})"

class TreqeAlgorithmCorregido:
    """
    Algoritmo Treqe con lógica económica CORRECTA
    """
    
    def __init__(self, time_budget_seconds: int = 300, max_k: int = 8):
        self.time_budget = time_budget_seconds
        self.max_k = max_k
        self.start_time = None
        self.users = []
        
    def create_realistic_users(self, n_users: int = 100, density: float = 0.05) -> List[TreqeUser]:
        """Crear usuarios realistas con densidad española (5% k=2)"""
        items_pool = [
            "iPhone 15 Pro", "Samsung S24", "MacBook Pro M3", "iPad Air",
            "Canon EOS R5", "Sony A7IV", "Nintendo Switch", "PlayStation 5",
            "Zapatos Nike", "Chaqueta North Face", "Bolso Michael Kors", 
            "Sofá 3 plazas", "Mesa comedor", "Bicicleta carretera", "Cinta correr"
        ]
        
        item_values = {
            "iPhone 15 Pro": 900, "Samsung S24": 800, "MacBook Pro M3": 1800,
            "iPad Air": 600, "Canon EOS R5": 2500, "Sony A7IV": 2200,
            "Nintendo Switch": 250, "PlayStation 5": 450,
            "Zapatos Nike": 80, "Chaqueta North Face": 120, 
            "Bolso Michael Kors": 150, "Sofá 3 plazas": 300,
            "Mesa comedor": 200, "Bicicleta carretera": 400,
            "Cinta correr": 350
        }
        
        # Categorías para preferencias realistas
        categories = {
            'tecnologia': ["iPhone 15 Pro", "Samsung S24", "MacBook Pro M3", "iPad Air", "Nintendo Switch", "PlayStation 5"],
            'fotografia': ["Canon EOS R5", "Sony A7IV"],
            'moda': ["Zapatos Nike", "Chaqueta North Face", "Bolso Michael Kors"],
            'hogar': ["Sofá 3 plazas", "Mesa comedor"],
            'deporte': ["Bicicleta carretera", "Cinta correr"]
        }
        
        users = []
        for user_id in range(n_users):
            # Usuario ofrece un item aleatorio
            offered_item = random.choice(items_pool)
            offered_value = item_values[offered_item]
            
            # Determinar categoría del item ofrecido
            offered_category = None
            for cat, items in categories.items():
                if offered_item in items:
                    offered_category = cat
                    break
            
            # Usuario quiere items de OTRAS categorías (realismo)
            wanted_items = []
            wanted_values = []
            
            # Número de items deseados (1-2, realista)
            n_wanted = random.randint(1, 2)
            
            # Elegir categorías diferentes a la ofrecida
            available_categories = [cat for cat in categories.keys() if cat != offered_category]
            if available_categories:
                for _ in range(n_wanted):
                    target_category = random.choice(available_categories)
                    # Solo incluir si hay densidad (5% probabilidad por item)
                    if random.random() < density:
                        available_items = [item for item in categories[target_category] if item != offered_item]
                        if available_items:
                            wanted_item = random.choice(available_items)
                            wanted_items.append(wanted_item)
                            wanted_values.append(item_values[wanted_item])
            
            # Si no hay items deseados (95% casos), añadir uno genérico
            if not wanted_items:
                generic_item = random.choice([item for item in items_pool if item != offered_item])
                wanted_items.append(generic_item)
                wanted_values.append(item_values[generic_item])
            
            users.append(TreqeUser(user_id, offered_item, offered_value, wanted_items, wanted_values))
        
        return users
    
    def build_preference_graph(self, users: List[TreqeUser]) -> Dict[int, Set[int]]:
        """Construir grafo de preferencias realista"""
        graph = defaultdict(set)
        item_to_owners = defaultdict(set)
        
        # Mapear cada item a sus dueños
        for user in users:
            item_to_owners[user.offered['item']].add(user.id)
        
        # Construir grafo con densidad realista
        for user in users:
            user_id = user.id
            for wanted in user.wanted:
                item = wanted['item']
                if item in item_to_owners:
                    for owner_id in item_to_owners[item]:
                        if owner_id != user_id:
                            graph[user_id].add(owner_id)
        
        return graph
    
    def find_cycles_k(self, graph: Dict[int, Set[int]], k: int, 
                     excluded_users: Set[int], time_remaining: float) -> List[Tuple[int, ...]]:
        """Encontrar ciclos de tamaño k (DFS limitado)"""
        cycles = []
        
        # Solo buscar entre usuarios no excluidos
        available_users = [uid for uid in graph.keys() if uid not in excluded_users]
        
        if len(available_users) < k:
            return cycles
        
        # Búsqueda DFS con profundidad limitada
        for start_user in available_users[:20]:  # Limitar para rendimiento
            if time.time() - self.start_time > self.time_budget - 10:
                break
                
            stack = [(start_user, [start_user], {start_user})]
            
            while stack:
                current_user, path, visited = stack.pop()
                
                # Si llegamos al tamaño k, verificar si cerramos ciclo
                if len(path) == k:
                    # Verificar si el último puede conectar con el primero
                    if start_user in graph.get(current_user, set()):
                        # Normalizar ciclo (empezar por el menor ID)
                        min_idx = path.index(min(path))
                        normalized = tuple(path[min_idx:] + path[:min_idx])
                        if normalized not in cycles:
                            cycles.append(normalized)
                    continue
                
                # Continuar búsqueda
                if len(path) < k:
                    neighbors = graph.get(current_user, set())
                    for neighbor in neighbors:
                        if neighbor not in visited and neighbor not in excluded_users:
                            new_path = path + [neighbor]
                            new_visited = visited.copy()
                            new_visited.add(neighbor)
                            stack.append((neighbor, new_path, new_visited))
        
        return cycles
    
    def select_best_cycles(self, cycles: List[Tuple[int, ...]], users: List[TreqeUser], 
                          already_matched: Set[int]) -> List[TreqeCycle]:
        """Seleccionar mejores ciclos según valor y compensaciones justas"""
        treqe_cycles = []
        
        for cycle_ids in cycles:
            # Verificar que no haya solapamiento
            cycle_set = set(cycle_ids)
            if cycle_set.intersection(already_matched):
                continue
            
            #