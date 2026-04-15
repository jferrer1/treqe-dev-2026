"""
Algoritmo Treqe Completo - Versión Funcional
Implementación completa con todos los métodos necesarios
"""

import time
import random
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict, deque
from datetime import datetime, timedelta
from sqlalchemy import select

from ..database.models import User, Item, Preference
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("core.algorithm_complete")

# ============================================================================
# ESTRUCTURAS DE DATOS
# ============================================================================

class TreqeUserComplete:
    """Usuario completo para algoritmo"""
    __slots__ = ['id', 'username', 'reputation', 'item_id', 'item_title', 
                 'item_value', 'desired_items_set', 'desired_keywords']
    
    def __init__(self, db_user: User, db_item: Item, db_preferences: List[Preference]):
        self.id = db_user.id
        self.username = db_user.username
        self.reputation = float(db_user.reputation_score)
        
        self.item_id = db_item.id
        self.item_title = db_item.title
        self.item_value = float(db_item.estimated_value)
        
        # Estructuras O(1) para matching rápido
        self.desired_items_set = set()
        self.desired_keywords = set()
        
        for pref in db_preferences:
            if pref.is_active:
                title_lower = pref.desired_item_title.lower()
                self.desired_items_set.add(title_lower)
                
                # Extraer palabras clave
                words = title_lower.split()
                for word in words[:4]:  # Primeras 4 palabras
                    if len(word) > 3:  # Ignorar palabras muy cortas
                        self.desired_keywords.add(word)
    
    def wants_item(self, item_title: str) -> bool:
        """Verificación de compatibilidad"""
        title_lower = item_title.lower()
        
        # 1. Verificación exacta
        if title_lower in self.desired_items_set:
            return True
        
        # 2. Verificación por keywords
        item_words = set(title_lower.split())
        return len(item_words & self.desired_keywords) >= 2
    
    def __repr__(self):
        return f"User{self.id}:{self.item_title[:20]}...€{self.item_value}"

class ExchangeCycleComplete:
    """Ciclo de intercambio completo"""
    __slots__ = ['user_ids', 'k', 'exchanges', 'total_value', 'total_commission']
    
    def __init__(self, user_ids: List[int], users: List[TreqeUserComplete], 
                 user_map: Dict[int, TreqeUserComplete]):
        self.user_ids = user_ids
        self.k = len(user_ids)
        self.exchanges = []
        self.total_value = 0
        self.total_commission = 0
        
        # Construir ciclo
        for i in range(self.k):
            current_id = user_ids[i]
            next_id = user_ids[(i + 1) % self.k]
            
            current_user = user_map[current_id]
            next_user = user_map[next_id]
            
            # Diferencia de valor
            value_diff = next_user.item_value - current_user.item_value
            
            # Comisión según reputación
            commission_rate = self._get_commission_rate(current_user.reputation)
            
            # Lógica económica correcta
            if value_diff > 0:
                # Recibe item de mayor valor → PAGA
                commission = value_diff * commission_rate
                payment = value_diff + commission
                
                compensation = {
                    'type': 'pays',
                    'amount': round(payment, 2),
                    'difference': round(value_diff, 2),
                    'commission': round(commission, 2),
                    'rate': round(commission_rate * 100, 1)
                }
            elif value_diff < 0:
                # Da item de mayor valor → RECIBE
                commission = abs(value_diff) * commission_rate
                receives = abs(value_diff) - commission
                
                compensation = {
                    'type': 'receives',
                    'amount': round(receives, 2),
                    'difference': round(value_diff, 2),
                    'commission': round(commission, 2),
                    'rate': round(commission_rate * 100, 1)
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
                'username': current_user.username,
                'gives': current_user.item_title,
                'gives_value': round(current_user.item_value, 2),
                'receives': next_user.item_title,
                'receives_value': round(next_user.item_value, 2),
                'compensation': compensation,
                'reputation': round(current_user.reputation, 1)
            }
            
            self.exchanges.append(exchange)
            self.total_value += current_user.item_value
            self.total_commission += compensation.get('commission', 0)
    
    def _get_commission_rate(self, reputation: float) -> float:
        """Comisiones escalonadas"""
        if reputation >= 80:
            return 0.04  # 4%
        elif reputation >= 60:
            return 0.06  # 6%
        else:
            return 0.08  # 8%
    
    def verify_economic_consistency(self) -> bool:
        """Verificar sistema cerrado"""
        total_payments = sum(e['compensation']['amount'] 
                           for e in self.exchanges 
                           if e['compensation']['type'] == 'pays')
        
        total_receives = sum(e['compensation']['amount']
                           for e in self.exchanges
                           if e['compensation']['type'] == 'receives')
        
        return abs(total_payments - total_receives - self.total_commission) < 0.01
    
    def generate_user_proposal(self, user_id: int) -> Dict[str, Any]:
        """Generar propuesta para usuario"""
        user_exchange = next(e for e in self.exchanges if e['user_id'] == user_id)
        comp = user_exchange['compensation']
        
        if comp['type'] == 'pays':
            proposal = {
                'title': f"Intercambio encontrado: Obtienes {user_exchange['receives']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) → Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Pagas €{comp['amount']} total (€{comp['difference']} diferencia + €{comp['commission']} comisión Treqe {comp['rate']}%)",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor, pagas €{comp['amount']} = NETO: €{user_exchange['gives_value']}",
                'economic_logic': "RECIBES item de MAYOR valor → PAGAS la diferencia"
            }
        elif comp['type'] == 'receives':
            proposal = {
                'title': f"Intercambio encontrado: Das {user_exchange['gives']} por {user_exchange['receives']} + €{comp['amount']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) → Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Recibes €{comp['amount']} (€{abs(comp['difference'])} diferencia - €{comp['commission']} comisión Treqe {comp['rate']}%)",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor + €{comp['amount']} = NETO: €{user_exchange['gives_value']}",
                'economic_logic': "DAS item de MAYOR valor → RECIBES la diferencia"
            }
        else:
            proposal = {
                'title': f"Intercambio perfecto: Das {user_exchange['gives']} por {user_exchange['receives']}",
                'summary': f"Intercambio igualitario: {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': "Sin ajuste monetario (valores iguales)",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor = NETO: €{user_exchange['gives_value']}",
                'economic_logic': "Valores iguales → intercambio directo"
            }
        
        # Metadata
        proposal.update({
            'exchange_id': f"treqe_{int(time.time())}_{user_id}",
            'exchange_type': 'circular',
            'k_size': self.k,
            'total_participants': self.k,
            'participants_info': [f"Usuario {e['username']}: {e['gives']} → {e['receives']}" 
                                 for e in self.exchanges if e['user_id'] != user_id],
            'generated_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
            'algorithm_version': 'complete_v1'
        })
        
        return proposal
    
    def __repr__(self):
        return f"Cycle(k={self.k}, users={self.user_ids}, value=€{self.total_value:.0f})"

# ============================================================================
# ALGORITMO PRINCIPAL COMPLETO
# ============================================================================

class TreqeMatchingEngineComplete:
    """
    Motor de matching completo con todos los métodos implementados
    """
    
    def __init__(self):
        self.k_max = 6  # Máximo k=6
        self.timeout_seconds = 5  # Timeout 5 segundos
        self.max_users_pool = 100
        self.max_cycles_per_k = 50
        self.cache_ttl = 300  # Cache 5 minutos
        self.cache = {}
        self.logger = get_logger("core.algorithm_complete")
        
        # Estadísticas
        self.stats = {
            'searches': 0,
            'cache_hits': 0,
            'cycles_found': defaultdict(int),
            'avg_search_time': 0
        }
    
    async def get_user_data(self, db, user_id: int) -> Optional[TreqeUserComplete]:
        """Obtener datos del usuario"""
        try:
            # Obtener usuario
            stmt_user = select(User).where(User.id == user_id)
            result_user = await db.execute(stmt_user)
            db_user = result_user.scalar_one_or_none()
            
            if not db_user:
                return None
            
            # Obtener item activo
            stmt_item = select(Item).where(
                Item.user_id == user_id,
                Item.status == "available"
            )
            result_item = await db.execute(stmt_item)
            db_item = result_item.scalar_one_or_none()
            
            if not db_item:
                return None
            
            # Obtener preferencias activas
            stmt_prefs = select(Preference).where(
                Preference.user_id == user_id,
                Preference.is_active == True
            )
            result_prefs = await db.execute(stmt_prefs)
            db_preferences = result_prefs.scalars().all()
            
            if not db_preferences:
                return None
            
            return TreqeUserComplete(db_user, db_item, db_preferences)
            
        except Exception as e:
            self.logger.error(f"Error getting user data: {e}")
            return None
    
    async def get_compatible_users_pool(self, db, target_user: TreqeUserComplete) -> List[TreqeUserComplete]:
        """Obtener pool de usuarios compatibles"""
        compatible_users = []
        
        try:
            # Obtener todos los usuarios activos (excepto el target)
            stmt_users = select(User).where(
                User.id != target_user.id
            ).limit(self.max_users_pool)
            
            result_users = await db.execute(stmt_users)
            db_users = result_users.scalars().all()
            
            for db_user in db_users:
                # Obtener item activo
                stmt_item = select(Item).where(
                    Item.user_id == db_user.id,
                    Item.status == "available"
                )
                result_item = await db.execute(stmt_item)
                db_item = result_item.scalar_one_or_none()
                
                if not db_item:
                    continue
                
                # Obtener preferencias activas
                stmt_prefs = select(Preference).where(
                    Preference.user_id == db_user.id,
                    Preference.is_active == True
                )
                result_prefs = await db.execute(stmt_prefs)
                db_preferences = result_prefs.scalars().all()
                
                if not db_preferences:
                    continue
                
                # Crear usuario Treqe
                treqe_user = TreqeUserComplete(db_user, db_item, db_preferences)
                
                # Verificar compatibilidad bidireccional
                if (target_user.wants_item(treqe_user.item_title) or 
                    treqe_user.wants_item(target_user.item_title)):
                    compatible_users.append(treqe_user)
            
            return compatible_users
            
        except Exception as e:
            self.logger.error(f"Error getting compatible users: {e}")
            return []
    
    def build_preference_graph_final(self, users: List[TreqeUserComplete]) -> Dict[int, Set[int]]:
        """Construir grafo de preferencias"""
        graph = defaultdict(set)
        user_map = {user.id: user for user in users}
        
        for user1 in users:
            for user2 in users:
                if user1.id == user2.id:
                    continue
                
                # Verificar si user1 quiere lo que tiene user2
                if user1.wants_item(user2.item_title):
                    graph[user1.id].add(user2.id)
        
        return graph
    
    def find_cycles_final(self, graph: Dict[int, Set[int]], k: int, 
                         matched_user_ids: Set[int], start_time: float) -> List[List[int]]:
        """Encontrar ciclos de tamaño k"""
        cycles = []
        nodes = list(graph.keys())
        
        # Filtrar nodos ya emparejados
        available_nodes = [n for n in nodes if n not in matched_user_ids]
        
        if len(available_nodes) < k:
            return cycles
        
        # Algoritmo DFS para encontrar ciclos
        def dfs(current: int, path: List[int], visited: Set[int]):
            if time.time() - start_time > self.timeout_seconds:
                return
            
            if len(path) == k:
                # Verificar si hay arco del último al primero
                if path[0] in graph.get(path[-1], set()):
                    # Normalizar ciclo (empezar por el ID más pequeño)
                    min_idx = path.index(min(path))
                    normalized = tuple(path[min_idx:] + path[:min_idx])
                    if normalized not in seen_cycles:
                        seen_cycles.add(normalized)
                        cycles.append(list(normalized))
                return
            
            if len(path) > k:
                return
            
            # Explorar vecinos
            for neighbor in graph.get(current, []):
                if neighbor not in visited and neighbor not in matched_user_ids:
                    dfs(neighbor, path + [neighbor], visited | {neighbor})
        
        seen_cycles = set()
        
        # Buscar ciclos desde cada nodo disponible
        for start_node in available_nodes[:20]:  # Limitar para performance
            if time.time() - start_time > self.timeout_seconds:
                break
            dfs(start_node, [start_node], {start_node})
        
        return cycles
    
    def get_optimal_search_order(self, user_count: int) -> List[int]:
        """Orden de búsqueda óptimo"""
        if user_count < 10:
            return [2, 3, 4]  # Pocos usuarios: buscar k pequeños
        elif user_count < 30:
            return [3, 4, 2, 5]  # k=3 más común, luego k=4
        else:
            return [3, 4, 5, 2, 6]  # k=3,4,5 más probables
    
    async def find_exchanges_for_user(self, db, user_id: int) -> List[Dict[str, Any]]:
        """Buscar intercambios para usuario"""
        start_time = time.time()
        self.stats['searches'] += 1
        
        # Verificar cache
        cache_key = f"user_{user_id}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                self.stats['cache_hits'] += 1
                self.logger.info(f"Cache hit for user {user_id}")
                return cache_entry['result']
        
        self.logger.info(f"Starting search for user {user_id}")
        
        try:
            # Obtener datos del usuario
            user_data = await self.get_user_data(db, user_id)
            if not user_data:
                return []
            
            # Obtener pool de usuarios compatibles
            compatible_users = await self.get_compatible_users_pool(db, user_data)
            self.logger.info(f"Compatible pool: {len(compatible_users)} users")
            
            if len(compatible_users) < 2:
                return []
            
            # Construir grafo
            graph = self.build_preference_graph_final(compatible_users)
            
            # Buscar ciclos
            found_cycles = []
            matched_user_ids = set()
            
            search_order = self.get_optimal_search_order(len(compatible_users))
            
            for k in search_order:
                if k > self.k_max:
                    break
                    
                if time.time() - start_time > self.timeout_seconds:
                    self.logger.warning(f"Timeout after {self.timeout_seconds}s")
                    break
                
                if k > len(compatible_users) - len(matched_user_ids):
                    continue
                
                self.logger.debug(f"Searching cycles k={k}")
                cycles = self.find_cycles_final(graph, k, matched_user_ids, start_time)
                
                for cycle_ids in cycles[:3]:  # Tomar máximo 3 ciclos por k
                    try:
                        cycle_users = [u for u in compatible_users if u.id in cycle_ids]
                        user_map = {u.id: u for u in compatible_users}
                        
                        cycle = ExchangeCycleComplete(list(cycle_ids), cycle_users, user_map)
                        
                        if cycle.verify_economic_consistency():
                            found_cycles.append(cycle)
                            matched_user_ids.update(cycle_ids)
                            self.stats['cycles_found'][k] += 1
                            
                            if len(found_cycles) >= 5:
                                break
                                
                    except Exception as e:
                        self.logger.error(f"Error processing cycle: {e}")
                        continue
                
                if len(found_cycles) >= 5:
                    break
            
            # Convertir a propuestas
            proposals = []
            for cycle in found_cycles:
                if user_id in cycle.user_ids:
                    proposal = cycle.generate_user_proposal(user_id)
                    proposals.append(proposal)
            
            search_time = time.time() - start_time
            self.stats['avg_search_time'] = (
                self.stats['avg_search_time'] * (self.stats['searches'] - 1) + search_time
            ) / self.stats['searches']
            
            self.logger.info(f"Search completed in {search_time:.2f}s. Found {len(proposals)} proposals")
            
            # Actualizar cache
            self.cache[cache_key] = {
                'result': proposals,
                'timestamp': time.time(),
                'search_time': search_time
            }
            
            return proposals
            
        except Exception as e:
            self.logger.error(f"Error in matching: {e}")
            return []
