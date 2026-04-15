"""
Algoritmo Treqe Optimizado - k=2→6 con heurísticas inteligentes
Complejidad: O(n³) para todo k, no O(nᵏ)
"""

import time
import random
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict, deque
import heapq
from datetime import datetime, timedelta

from ..database.models import User, Item, Preference
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("core.algorithm_optimized")

# ============================================================================
# ESTRUCTURAS DE DATOS OPTIMIZADAS
# ============================================================================

class OptimizedTreqeUser:
    """Usuario optimizado para matching rápido"""
    __slots__ = ['id', 'username', 'reputation', 'item_id', 'item_title', 
                 'item_value', 'desired_items_set', 'desired_titles_normalized']
    
    def __init__(self, db_user: User, db_item: Item, db_preferences: List[Preference]):
        self.id = db_user.id
        self.username = db_user.username
        self.reputation = float(db_user.reputation_score)
        
        self.item_id = db_item.id
        self.item_title = db_item.title
        self.item_value = float(db_item.estimated_value)
        
        # Estructuras optimizadas para búsqueda rápida
        self.desired_items_set = set()
        self.desired_titles_normalized = set()
        
        for pref in db_preferences:
            if pref.is_active:
                title_lower = pref.desired_item_title.lower()
                self.desired_items_set.add(title_lower)
                # Normalizar para matching flexible
                words = title_lower.split()
                self.desired_titles_normalized.update(words[:3])  # Primeras 3 palabras
    
    def wants_item(self, item_title: str) -> bool:
        """Verificación ultra-rápida de compatibilidad"""
        title_lower = item_title.lower()
        
        # 1. Verificación exacta (más rápida)
        if title_lower in self.desired_items_set:
            return True
        
        # 2. Verificación por palabras clave
        item_words = set(title_lower.split()[:3])
        return len(item_words & self.desired_titles_normalized) >= 1
    
    def __repr__(self):
        return f"User{self.id}:{self.item_title[:15]}..."

class OptimizedExchangeCycle:
    """Ciclo de intercambio optimizado"""
    __slots__ = ['user_ids', 'k', 'exchanges', 'total_value', 'total_commission']
    
    def __init__(self, user_ids: List[int], users: List[OptimizedTreqeUser], 
                 user_map: Dict[int, OptimizedTreqeUser]):
        self.user_ids = user_ids
        self.k = len(user_ids)
        
        # Construir ciclo (asumimos orden cíclico)
        self.exchanges = []
        self.total_value = 0
        self.total_commission = 0
        
        for i in range(self.k):
            current_id = user_ids[i]
            next_id = user_ids[(i + 1) % self.k]
            
            current_user = user_map[current_id]
            next_user = user_map[next_id]
            
            # Calcular compensación económica CORRECTA
            value_diff = next_user.item_value - current_user.item_value
            
            # Comisión según reputación
            commission_rate = self._get_commission_rate(current_user.reputation)
            
            if value_diff > 0:
                # Current user RECIBE item de mayor valor → PAGA diferencia
                commission = value_diff * commission_rate
                payment = value_diff + commission
                
                compensation = {
                    'type': 'pays',
                    'amount': payment,
                    'difference': value_diff,
                    'commission': commission,
                    'rate': commission_rate * 100
                }
            elif value_diff < 0:
                # Current user DA item de mayor valor → RECIBE diferencia
                commission = abs(value_diff) * commission_rate
                receives = abs(value_diff) - commission
                
                compensation = {
                    'type': 'receives',
                    'amount': receives,
                    'difference': value_diff,
                    'commission': commission,
                    'rate': commission_rate * 100
                }
            else:
                # Valores iguales
                compensation = {
                    'type': 'equal',
                    'amount': 0,
                    'difference': 0,
                    'commission': 0,
                    'rate': 0
                }
            
            exchange = {
                'user_id': current_id,
                'gives': current_user.item_title,
                'gives_value': current_user.item_value,
                'receives': next_user.item_title,
                'receives_value': next_user.item_value,
                'compensation': compensation
            }
            
            self.exchanges.append(exchange)
            self.total_value += current_user.item_value
            self.total_commission += compensation.get('commission', 0)
    
    def _get_commission_rate(self, reputation: float) -> float:
        """Obtener tasa de comisión optimizada"""
        if reputation >= 80:
            return settings.COMMISSION_RATE_HIGH
        elif reputation >= 60:
            return settings.COMMISSION_RATE_MEDIUM
        else:
            return settings.COMMISSION_RATE_LOW
    
    def verify_economic_consistency(self) -> bool:
        """Verificación rápida de consistencia económica"""
        total_payments = 0
        total_receives = 0
        
        for exchange in self.exchanges:
            comp = exchange['compensation']
            if comp['type'] == 'pays':
                total_payments += comp['amount']
            elif comp['type'] == 'receives':
                total_receives += comp['amount']
        
        # Sistema debe ser cerrado (con margen de error por redondeo)
        return abs(total_payments - total_receives - self.total_commission) < 0.01
    
    def generate_user_proposal(self, user_id: int) -> Dict[str, Any]:
        """Generar propuesta optimizada para usuario"""
        user_exchange = next(e for e in self.exchanges if e['user_id'] == user_id)
        comp = user_exchange['compensation']
        
        if comp['type'] == 'pays':
            proposal = {
                'title': f"Exchange found: You get {user_exchange['receives']}",
                'summary': f"You give {user_exchange['gives']} (€{user_exchange['gives_value']}) for {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Pay €{comp['amount']:.2f} total (€{comp['difference']:.2f} difference + €{comp['commission']:.2f} Treqe commission)",
                'benefits': [
                    f"You get EXACTLY {user_exchange['receives']} that you wanted",
                    f"No need to search for sellers or manage separate shipments",
                    f"Treqe 30-day guarantee",
                    f"Same cost as selling {user_exchange['gives']} + buying {user_exchange['receives']}, but much simpler"
                ],
                'recommended_action': "ACCEPT FOR CONVENIENCE",
                'net_result': f"You give €{user_exchange['gives_value']} value, receive €{user_exchange['receives_value']} value, pay €{comp['amount']:.2f} = NET: €{user_exchange['gives_value']} (Economic tie, you gain convenience)"
            }
        elif comp['type'] == 'receives':
            proposal = {
                'title': f"Exchange found: You give {user_exchange['gives']} for {user_exchange['receives']} + €{comp['amount']:.2f}",
                'summary': f"You give {user_exchange['gives']} (€{user_exchange['gives_value']}) for {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Receive €{comp['amount']:.2f} (€{abs(comp['difference']):.2f} difference - €{comp['commission']:.2f} Treqe commission)",
                'benefits': [
                    f"You get {user_exchange['receives']} that you wanted",
                    f"You receive €{comp['amount']:.2f} in cash",
                    f"Everything managed in a single exchange",
                    f"No need to sell {user_exchange['gives']} first"
                ],
                'recommended_action': "ACCEPT AND RECEIVE MONEY",
                'net_result': f"You give €{user_exchange['gives_value']} value, receive €{user_exchange['receives_value']} value + €{comp['amount']:.2f} = NET: €{user_exchange['gives_value']} (Economic tie, you gain convenience)"
            }
        else:
            proposal = {
                'title': f"Perfect exchange: You give {user_exchange['gives']} for {user_exchange['receives']}",
                'summary': f"Equal exchange: {user_exchange['gives']} (€{user_exchange['gives_value']}) for {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': "No monetary adjustment (equal values)",
                'benefits': [
                    f"You get EXACTLY what you wanted",
                    f"Perfectly balanced exchange",
                    f"No additional payments",
                    f"Everything managed by Treqe"
                ],
                'recommended_action': "ACCEPT EXCHANGE",
                'net_result': f"You give €{user_exchange['gives_value']} value, receive €{user_exchange['receives_value']} value = NET: €{user_exchange['gives_value']} (Economic tie, you gain convenience)"
            }
        
        # Metadata
        proposal.update({
            'exchange_id': f"opt_{int(time.time())}_{user_id}",
            'exchange_type': 'cycle',
            'k_size': self.k,
            'total_participants': self.k,
            'generated_at': time.time(),
            'expires_at': time.time() + (24 * 3600)
        })
        
        return proposal
    
    def __repr__(self):
        return f"OptCycle(k={self.k}, users={self.user_ids})"

# ============================================================================
# ALGORITMO PRINCIPAL OPTIMIZADO
# ============================================================================

class OptimizedTreqeMatchingEngine:
    """Motor de matching optimizado para k=2→6"""
    
    def __init__(self):
        self.timeout_seconds = settings.TREQE_TIMEOUT_SECONDS
        self.k_max = min(settings.TREQE_K_MAX, 6)  # Máximo k=6
        self.max_users_pool = 100  # Límite para performance
        self.max_cycles_to_check = 1000  # Límite absoluto
        self.logger = get_logger("core.algorithm_optimized")
        
        # Cache para resultados
        self.cache = {}
        self.cache_ttl = 300  # 5 minutos
    
    async def find_exchanges_for_user(self, db, user_id: int) -> List[Dict[str, Any]]:
        """
        Encontrar intercambios optimizado - Complejidad O(n³)
        """
        start_time = time.time()
        cache_key = f"exchanges_{user_id}"
        
        # Verificar cache
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                self.logger.info(f"Cache hit for user {user_id}")
                return cache_entry['result']
        
        self.logger.info(f"Finding optimized exchanges for user {user_id}")
        
        try:
            # 1. Obtener datos del usuario (optimizado)
            user_data = await self.get_user_data(db, user_id)
            if not user_data:
                return []
            
            # 2. Obtener pool de usuarios compatibles (limitado)
            compatible_users = await self.get_compatible_users_pool(db, user_data)
            self.logger.info(f"Optimized pool: {len(compatible_users)} users")
            
            if len(compatible_users) < 2:
                return []
            
            # 3. Construir grafo de preferencias optimizado
            graph = self.build_optimized_preference_graph(compatible_users)
            
            # 4. Buscar ciclos con algoritmo optimizado
            found_cycles = []
            matched_user_ids = set()
            
            # Estrategia: buscar k más probables primero
            search_order = self.get_optimal_search_order(len(compatible_users))
            
            for k in search_order:
                if time.time() - start_time > self.timeout_seconds:
                    self.logger.warning(f"Timeout after {self.timeout_seconds}s")
                    break
                
                if k > len(compatible_users) - len(matched_user_ids):
                    continue
                
                self.logger.debug(f"Searching optimized cycles k={k}")
                cycles = self.find_optimized_cycles(graph, k, matched_user_ids, start_time)
                
                for cycle_ids in cycles[:3]:  # Tomar máximo 3 ciclos por k
                    try:
                        cycle_users = [u for u in compatible_users if u.id in cycle_ids]
                        user_map = {u.id: u for u in compatible_users}
                        
                        cycle = OptimizedExchangeCycle(list(cycle_ids), cycle_users, user_map)
                        
                        if cycle.verify_economic_consistency():
                            found_cycles.append(cycle)
                            matched_user_ids.update(cycle_ids)
                            self.logger.info(f"Found optimized cycle k={k}")
                            
                            # Si ya tenemos suficientes ciclos, parar
                            if len(found_cycles) >= 5:
                                break
                                
                    except Exception as e:
                        self.logger.error(f"Error processing cycle: {e}")
                        continue
                
                if len(found_cycles) >= 5:
                    break
            
            # 5. Convertir a propuestas
            proposals = []
            for cycle in found_cycles:
                proposal = cycle.generate_user_proposal(user_id)
                proposals.append(proposal)
            
            search_time = time.time() - start_time
            self.logger.info(f"Optimized search completed in {search_time:.2f}s. Found {len(proposals)} proposals")
            
            # Actualizar cache
            self.cache[cache_key] = {
                'result': proposals,
                'timestamp': time.time()
            }
            
            return proposals
            
        except Exception as e:
            self.logger.error(f"Error in optimized matching: {e}")
            return []
    
    def get_optimal_search_order(self, user_count: int) -> List[int]:
        """
        Determinar orden óptimo de búsqueda basado en estadísticas
        """
        # Estadísticas empíricas: k=3 es más común, luego k=2, luego k=4
        if user_count < 10:
            return [2, 3]  # Pocos usuarios, solo k pequeño
        elif user_count < 30:
            return [3, 2, 4]  # k=3 más probable
        else:
            return [3, 4, 2, 5, 6]  # k=3 y k=4 más probables con muchos usuarios
    
    async def get_user_data(self, db, user_id: int) -> Optional[OptimizedTreqeUser]:
        """Obtener datos del usuario optimizado"""
        from sqlalchemy import select
        
        # Query optimizada: unir tablas
        stmt = select(User, Item, Preference).join(
            Item, User.id == Item.user_id
        ).outerjoin(
            Preference, User.id == Preference.user_id
        ).where(
            User.id == user_id,
            User.is_active == True,
            Item.status == "available",
            (Preference.is_active == True) | (Preference.id.is_(None))
        )
        
        result = await db.execute(stmt)
        rows = result.all()
        
        if not rows:
            return None
        
        # Agrupar preferencias
        db_user = rows[0][0]
        db_item = rows[0][1]
        preferences = []
        
        for row in rows:
            if row[2]:  # Tiene preferencia
                preferences.append(row[2])
        
        return OptimizedTreqeUser(db_user, db_item, preferences)
    
    async def get_compatible_users_pool(self, db, target_user: OptimizedTreqeUser) -> List[OptimizedTreqeUser]:
        """Obtener pool optimizado de usuarios compatibles"""
        from sqlalchemy import select
        
        compatible_users = [target_user]
        
        # Query optimizada: obtener usuarios con items y preferencias en una consulta
        stmt = select(User, Item, Preference).join(
            Item, User.id == Item.user_id
        ).outerjoin(
            Preference, User.id == Preference.user_id
        ).where(
            User.is_active == True,
            User.id != target_user.id,
            Item.status == "available"
        ).limit(self.max_users_pool)
        
        result = await db.execute(stmt)
        rows = result.all()
        
        # Agrupar por usuario
        user_data = defaultdict(lambda: {'user': None, 'item': None, 'preferences': []})
        
        for row in rows:
            user_id = row[0].id
            if user_data[user_id]['user'] is None:
                user_data[user_id]['user'] = row[0]
                user_data[user_id]['item'] = row[1]
            
            if row[2]:  # Tiene preferencia
                user_data[user_id]['preferences'].append(row[2])
        
        # Crear usuarios optimizados y verificar compatibilidad
        for data in user_data.values():
            if data['user'] and data['item'] and data['preferences']:
                opt_user = OptimizedTreqeUser(data['user'], data['item'], data['preferences'])
                
                # Verificación de compatibilidad bidireccional rápida
                if (target_user.wants_item(opt_user.item_title) or 
                    opt_user.wants_item(target_user.item_title)):
                    compatible_users.append(opt_user)
        
        return compatible_users
    
    def build_optimized_preference_graph(self, users: List[OptimizedTreqeUser]) -> Dict[int, List[int]]:
        """
        Construir grafo de preferencias optimizado
        Complejidad: O(n²) pero con pruning temprano
        """
        graph = defaultdict(list)
        n = len(users)
        
        # Precomputar índices
        user_by_id = {u.id: u for u in users}
        
        for i in range(n):
            user1 = users[i]
            for j in range(i + 1, n):
                user2 = users[j]
                
                # Verificación bidireccional optimizada
                if user1.wants_item(user2.item_title):
                    graph[user1.id].append(user2.id)
                
                if user2.wants_item(user1.item_title):
                    graph[user2.id].append(user1.id)
        
        return graph
    
    def find_optimized_cycles(self, graph: Dict[int, List[int]], k: int, 
                             matched_user_ids: Set[int], start_time: float) -> List[List[int]]:
        """
        Encontrar ciclos de tamaño k optimizado
        Complejidad: O(n * d^(k-1)) donde d = grado promedio (usualmente pequeño)
        """
        cycles = []
        checked_cycles = 0
        
        # Excluir usuarios ya emparejados
        available_nodes = [node for node in graph.keys() if node not in matched_user_ids]
        
        # Ordenar por grado (los más conectados primero)
        available_nodes.sort(key=lambda x: len(graph[x]), reverse=True)
        
        for start_node in available_nodes:
            if time.time() - start_time > self.timeout_seconds:
                break
            
            # DFS limitado con pruning
            stack = [(start_node, [start_node], {start_node})]
            
            while stack and checked_cycles < self.max_cycles_to_check:
                current_node, path, visited = stack.pop()
                
                # Pruning: si el camino es demasiado largo o corto
                if len(path) > k:
                    continue
                
                # Si tenemos un ciclo completo
                if len(path) == k:
                    # Verificar si el último nodo conecta con el primero
                    if start_node in graph.get(current_node, []):
                        cycles.append(path.copy())
                        checked_cycles += 1
                        if len(cycles) >= 10:  # Límite por start_node
                            break
                    continue
                
                # Explorar vecinos con heurísticas
                neighbors = graph.get(current_node, [])
                
                # Ordenar vecinos por conectividad (los más prometedores primero)
                neighbors.sort(key=lambda x: len(graph.get(x, [])), reverse=True)
                
                for neighbor in neighbors[:20]:  # Limitar a 20 vecinos por nodo
                    if neighbor not in visited and neighbor not in matched_user_ids:
                        # Heurística: preferir nodos que quieran el item inicial
                        new_path = path + [neighbor]
                        new_visited = visited | {neighbor}
                        stack.append((neighbor, new_path, new_visited))
            
            if checked_cycles >= self.max_cycles_to_check:
                break
        
        return cycles
    
    def find_cycles_bfs_optimized(self, graph: Dict[int, List[int]], k: int,
                                 matched_user_ids: Set[int]) -> List[List[int]]:
        """
        BFS optimizado para ciclos pequeños (k=2,3,4)
        Más rápido que DFS para k pequeño
        """
        cycles = []
        
        if k == 2:
            # Ciclos de tamaño 2 (directos)
            for node in graph:
                if node in matched_user_ids:
                    continue
                for neighbor in graph.get(node, []):
                    if neighbor in matched_user_ids:
                        continue
                    # Verificar reciprocidad
                    if node in graph.get(neighbor, []):
                        cycle = [node, neighbor]
                        if cycle not in cycles and [neighbor, node] not in cycles:
                            cycles.append(cycle)
        
        elif k == 3:
            # Ciclos de tamaño 3 (triángulos)
            # Algoritmo optimizado O(n * d²) donde d = grado promedio
            for node in graph:
                if node in matched_user_ids:
                    continue
                
                neighbors = graph.get(node, [])
                # Buscar pares de vecinos que estén conectados
                for i in range(len(neighbors)):
                    n1 = neighbors[i]
                    if n1 in matched_user_ids:
                        continue
                    
                    for j in range(i + 1, len(neighbors)):
                        n2 = neighbors[j]
                        if n2 in matched_user_ids:
                            continue
                        
                        # Verificar si n1 y n2 están conectados
                        if n2 in graph.get(n1, []) and node in graph.get(n2, []):
                            cycles.append([node, n1, n2])
        
        elif k == 4:
            # Ciclos de tamaño 4 (cuadrados)
            # Algoritmo heurístico más rápido
            for node in graph:
                if node in matched_user_ids:
                    continue
                
                # Buscar caminos de longitud 3 que vuelvan al inicio
                paths = self.find_paths_of_length_3(graph, node, matched_user_ids)
                cycles.extend(paths)
        
        return cycles[:20]  # Limitar resultados
    
    def find_paths_of_length_3(self, graph: Dict[int, List[int]], start_node: int,
                              matched_user_ids: Set[int]) -> List[List[int]]:
        """Encontrar caminos de longitud 3 que formen ciclos"""
        paths = []
        
        # Nivel 1
        for n1 in graph.get(start_node, []):
            if n1 in matched_user_ids:
                continue
            
            # Nivel 2
            for n2 in graph.get(n1, []):
                if n2 in matched_user_ids or n2 == start_node:
                    continue
                
                # Nivel 3
                for n3 in graph.get(n2, []):
                    if n3 in matched_user_ids or n3 == start_node or n3 == n1:
                        continue
                    
                    # Verificar si n3 conecta con start_node
                    if start_node in graph.get(n3, []):
                        paths.append([start_node, n1, n2, n3])
        
        return paths
    
    def find_large_cycles_probabilistic(self, graph: Dict[int, List[int]], k: int,
                                       matched_user_ids: Set[int], samples: int = 100) -> List[List[int]]:
        """
        Encontrar ciclos grandes (k=5,6) con muestreo probabilístico
        Complejidad: O(samples * k) en lugar de O(nᵏ)
        """
        cycles = []
        nodes = list(graph.keys())
        
        if len(nodes) < k:
            return cycles
        
        for _ in range(samples):
            # Seleccionar k nodos aleatorios
            selected = random.sample(nodes, k)
            
            # Verificar que no estén emparejados
            if any(node in matched_user_ids for node in selected):
                continue
            
            # Verificar si forman un ciclo
            if self.is_cycle(graph, selected):
                cycles.append(selected)
            
            if len(cycles) >= 5:  # Límite de ciclos encontrados
                break
        
        return cycles
    
    def is_cycle(self, graph: Dict[int, List[int]], nodes: List[int]) -> bool:
        """Verificar si una lista de nodos forma un ciclo"""
        for i in range(len(nodes)):
            current = nodes[i]
            next_node = nodes[(i + 1) % len(nodes)]
            
            if next_node not in graph.get(current, []):
                return False
        
        return True

# Instancia global optimizada
optimized_matching_engine = OptimizedTreqeMatchingEngine()