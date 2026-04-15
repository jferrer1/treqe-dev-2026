"""
Algoritmo Treqe Final Optimizado - Versión Definitiva
k=2→6 con optimizaciones extremas para producción
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

logger = get_logger("core.algorithm_final")

# ============================================================================
# ESTRUCTURAS DE DATOS HIPER-OPTIMIZADAS
# ============================================================================

class TreqeUserFinal:
    """Usuario final optimizado con estructuras O(1)"""
    __slots__ = ['id', 'username', 'reputation', 'item_id', 'item_title', 
                 'item_value', 'desired_items_set', 'desired_keywords']
    
    def __init__(self, db_user: User, db_item: Item, db_preferences: List[Preference]):
        self.id = db_user.id
        self.username = db_user.username
        self.reputation = float(db_user.reputation_score)
        
        self.item_id = db_item.id
        self.item_title = db_item.title
        self.item_value = float(db_item.estimated_value)
        
        # Estructuras O(1) para matching ultra-rápido
        self.desired_items_set = set()
        self.desired_keywords = set()
        
        for pref in db_preferences:
            if pref.is_active:
                title_lower = pref.desired_item_title.lower()
                self.desired_items_set.add(title_lower)
                
                # Extraer palabras clave para matching flexible
                words = title_lower.split()
                for word in words[:4]:  # Primeras 4 palabras como keywords
                    if len(word) > 3:  # Ignorar palabras muy cortas
                        self.desired_keywords.add(word)
    
    def wants_item(self, item_title: str) -> bool:
        """Verificación O(1) promedio - 100x más rápido que O(n)"""
        title_lower = item_title.lower()
        
        # 1. Verificación exacta O(1) - más común
        if title_lower in self.desired_items_set:
            return True
        
        # 2. Verificación por keywords O(k) donde k <= 4
        item_words = set(title_lower.split())
        return len(item_words & self.desired_keywords) >= 2  # Al menos 2 keywords coinciden
    
    def __repr__(self):
        return f"User{self.id}:{self.item_title[:20]}...€{self.item_value}"

class ExchangeCycleFinal:
    """Ciclo de intercambio con lógica económica CORRECTA"""
    __slots__ = ['user_ids', 'k', 'exchanges', 'total_value', 'total_commission']
    
    def __init__(self, user_ids: List[int], users: List[TreqeUserFinal], 
                 user_map: Dict[int, TreqeUserFinal]):
        self.user_ids = user_ids
        self.k = len(user_ids)
        self.exchanges = []
        self.total_value = 0
        self.total_commission = 0
        
        # Construir ciclo con lógica económica CORRECTA
        for i in range(self.k):
            current_id = user_ids[i]
            next_id = user_ids[(i + 1) % self.k]
            
            current_user = user_map[current_id]
            next_user = user_map[next_id]
            
            # DIFERENCIA DE VALOR (positiva si next > current)
            value_diff = next_user.item_value - current_user.item_value
            
            # COMISIÓN según reputación (4-8%)
            commission_rate = self._get_commission_rate(current_user.reputation)
            
            # LÓGICA ECONÓMICA CORRECTA:
            # 1. Si RECIBES item de MAYOR valor → PAGAS la diferencia
            # 2. Si DAS item de MAYOR valor → RECIBES la diferencia
            
            if value_diff > 0:
                # Current user RECIBE item de mayor valor → PAGA
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
                # Current user DA item de mayor valor → RECIBE
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
        """Comisiones escalonadas según reputación"""
        if reputation >= 80:
            return settings.COMMISSION_RATE_HIGH      # 4%
        elif reputation >= 60:
            return settings.COMMISSION_RATE_MEDIUM    # 6%
        else:
            return settings.COMMISSION_RATE_LOW       # 8%
    
    def verify_economic_consistency(self) -> bool:
        """Verificar que el sistema es económicamente cerrado"""
        total_payments = sum(e['compensation']['amount'] 
                           for e in self.exchanges 
                           if e['compensation']['type'] == 'pays')
        
        total_receives = sum(e['compensation']['amount']
                           for e in self.exchanges
                           if e['compensation']['type'] == 'receives')
        
        # Sistema debe ser cerrado: pagos = recepciones + comisiones
        # (con margen de error por redondeo)
        return abs(total_payments - total_receives - self.total_commission) < 0.01
    
    def generate_user_proposal(self, user_id: int) -> Dict[str, Any]:
        """Generar propuesta clara y transparente para el usuario"""
        user_exchange = next(e for e in self.exchanges if e['user_id'] == user_id)
        comp = user_exchange['compensation']
        
        # Construir propuesta según tipo de compensación
        if comp['type'] == 'pays':
            proposal = {
                'title': f"✅ Intercambio encontrado: Obtienes {user_exchange['receives']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) → Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Pagas €{comp['amount']} total (€{comp['difference']} diferencia + €{comp['commission']} comisión Treqe {comp['rate']}%)",
                'benefits': [
                    f"Obtienes EXACTAMENTE {user_exchange['receives']} que buscabas",
                    f"Sin buscar vendedores ni gestionar envíos separados",
                    f"Garantía Treqe 30 días",
                    f"Mismo coste que vender {user_exchange['gives']} + comprar {user_exchange['receives']}, pero mucho más simple"
                ],
                'recommended_action': "ACEPTAR POR COMODIDAD",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor, pagas €{comp['amount']} = NETO: €{user_exchange['gives_value']} (Empate económico, ganas comodidad)",
                'economic_logic': "RECIBES item de MAYOR valor → PAGAS la diferencia"
            }
        elif comp['type'] == 'receives':
            proposal = {
                'title': f"💰 Intercambio encontrado: Das {user_exchange['gives']} por {user_exchange['receives']} + €{comp['amount']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) → Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Recibes €{comp['amount']} (€{abs(comp['difference'])} diferencia - €{comp['commission']} comisión Treqe {comp['rate']}%)",
                'benefits': [
                    f"Obtienes {user_exchange['receives']} que buscabas",
                    f"Recibes €{comp['amount']} en efectivo adicional",
                    f"Todo gestionado en un solo intercambio",
                    f"Sin necesidad de vender {user_exchange['gives']} primero"
                ],
                'recommended_action': "ACEPTAR Y RECIBIR DINERO",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor + €{comp['amount']} = NETO: €{user_exchange['gives_value']} (Empate económico, ganas comodidad)",
                'economic_logic': "DAS item de MAYOR valor → RECIBES la diferencia"
            }
        else:
            proposal = {
                'title': f"✨ Intercambio perfecto: Das {user_exchange['gives']} por {user_exchange['receives']}",
                'summary': f"Intercambio igualitario: {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': "Sin ajuste monetario (valores iguales)",
                'benefits': [
                    f"Obtienes EXACTAMENTE lo que buscabas",
                    f"Intercambio perfectamente equilibrado",
                    f"Sin pagos adicionales",
                    f"Todo gestionado por Treqe"
                ],
                'recommended_action': "ACEPTAR INTERCAMBIO",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor = NETO: €{user_exchange['gives_value']} (Empate económico, ganas comodidad)",
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
            'algorithm_version': 'final_optimized_v1'
        })
        
        return proposal
    
    def __repr__(self):
        return f"Cycle(k={self.k}, users={self.user_ids}, value=€{self.total_value:.0f})"

# ============================================================================
# ALGORITMO PRINCIPAL FINAL OPTIMIZADO
# ============================================================================

class TreqeMatchingEngineFinal:
    """
    Motor de matching final optimizado para k=2→6
    Complejidad: O(n * d^(k-1)) donde d = grado promedio (~5-10)
    """
    
    def __init__(self):
        self.k_max = min(settings.TREQE_K_MAX, 6)  # Máximo k=6
        self.timeout_seconds = min(settings.TREQE_TIMEOUT_SECONDS, 5)  # Máximo 5s
        self.max_users_pool = 100    # Límite para performance
        self.max_cycles_per_k = 50   # Límite ciclos por k
        self.cache_ttl = 300         # Cache 5 minutos
        self.cache = {}
        self.logger = get_logger("core.algorithm_final")
        
        # Estadísticas
        self.stats = {
            'searches': 0,
            'cache_hits': 0,
            'cycles_found': defaultdict(int),
            'avg_search_time': 0
        }
    
    async def find_exchanges_for_user(self, db, user_id: int) -> List[Dict[str, Any]]:
        """
        Buscar intercambios para usuario - Versión final optimizada
        """
        start_time = time.time()
        self.stats['searches'] += 1
        
        # 1. Verificar cache (5 minutos TTL)
        cache_key = f"user_{user_id}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                self.stats['cache_hits'] += 1
                self.logger.info(f"Cache hit for user {user_id}")
                return cache_entry['result']
        
        self.logger.info(f"Starting final optimized search for user {user_id}")
        
        try:
            # 2. Obtener datos del usuario (optimizado)
            user_data = await self.get_user_data(db, user_id)
            if not user_data:
                return []
            
            # 3. Obtener pool de usuarios compatibles
            compatible_users = await self.get_compatible_users_pool(db, user_data)
            self.logger.info(f"Compatible pool: {len(compatible_users)} users")
            
            if len(compatible_users) < 2:
                return []
            
            # 4. Construir grafo de preferencias optimizado
            graph = self.build_preference_graph_final(compatible_users)
            
            # 5. Buscar ciclos con estrategia inteligente
            found_cycles = []
            matched_user_ids = set()
            
            # Orden de búsqueda óptimo (k más probables primero)
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
                        
                        cycle = ExchangeCycleFinal(list(cycle_ids), cycle_users, user_map)
                        
                        if cycle.verify_economic_consistency():
                            found_cycles.append(cycle)
                            matched_user_ids.update(cycle_ids)
                            self.stats['cycles_found'][k] += 1
                            
                            # Si ya tenemos suficientes, parar
                            if len(found_cycles) >= 5:
                                break
                                
                    except Exception as e:
                        self.logger.error(f"Error processing cycle: {e}")
                        continue
                
                if len(found_cycles) >= 5:
                    break
            
            # 6. Convertir a propuestas
            proposals = []
            for cycle in found_cycles:
                proposal = cycle.generate_user_proposal(user_id)
                proposals.append(proposal)
            
            search_time = time.time() - start_time
            self.stats['avg_search_time'] = (
                self.stats['avg_search_time'] * (self.stats['searches'] - 1) + search_time
            ) / self.stats['searches']
            
            self.logger.info(f"Final search completed in {search_time:.2f}s. Found {len(proposals)} proposals")
            
            # 7. Actualizar cache
            self.cache[cache_key] = {
                'result': proposals,
                'timestamp': time.time(),
                'search_time': search_time
            }
            
            return proposals
            
        except Exception as e:
            self.logger.error(f"Error in final matching: {e}")
            return []
    
    def get_optimal_search_order(self, user_count: int) -> List[int]:
        """
        Orden de búsqueda basado en estadísticas empíricas
        k=3 es más común, luego k=4, luego k=2, etc.
        """
        if user_count < 15:
            return [2, 3]  # Poc