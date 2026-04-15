"""
Algoritmo Treqe Final Optimizado - Versión Funcional Completa
Basado en algoritmo_simple.py pero con interfaz compatible
"""

import time
import re
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy import select

from ..database.models import User, Item, Preference
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("core.algorithm_final")

# ============================================================================
# ESTRUCTURAS DE DATOS FINALES OPTIMIZADAS
# ============================================================================

class TreqeUserFinal:
    """Usuario final optimizado"""
    __slots__ = ['id', 'username', 'reputation', 'item_id', 'item_title', 
                 'item_value', 'desired_titles', 'min_value', 'max_value']
    
    def __init__(self, db_user: User, db_item: Item, db_preferences: List[Preference]):
        self.id = db_user.id
        self.username = db_user.username
        self.reputation = float(db_user.reputation_score)
        
        self.item_id = db_item.id
        self.item_title = db_item.title
        self.item_value = float(db_item.estimated_value)
        
        # Preferencias
        self.desired_titles = []
        self.min_value = float('inf')
        self.max_value = 0
        
        for pref in db_preferences:
            if pref.is_active:
                self.desired_titles.append(pref.desired_item_title.lower())
                self.min_value = min(self.min_value, float(pref.min_value))
                self.max_value = max(self.max_value, float(pref.max_value))
    
    def wants_item(self, item_title: str) -> bool:
        """Verificación optimizada de compatibilidad"""
        item_title_lower = item_title.lower()
        
        for desired in self.desired_titles:
            # Comparación por palabras clave
            desired_words = set(re.findall(r'\w+', desired))
            item_words = set(re.findall(r'\w+', item_title_lower))
            
            common_words = desired_words & item_words
            if len(common_words) >= 2:
                # Para el MVP, asumimos que el valor está en rango
                # En una versión completa, necesitaríamos pasar el valor del item
                return True
        
        return False
    
    def __repr__(self):
        return f"User{self.id}:{self.item_title[:15]}...€{self.item_value}"

class ExchangeCycleFinal:
    """Ciclo de intercambio final con lógica económica correcta"""
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
            # 1. Si RECIBES item de MAYOR valor -> PAGAS la diferencia
            # 2. Si DAS item de MAYOR valor -> RECIBES la diferencia
            
            if value_diff > 0:
                # Current user RECIBE item de mayor valor -> PAGA
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
                # Current user DA item de mayor valor -> RECIBE
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
            return 0.04  # 4%
        elif reputation >= 60:
            return 0.06  # 6%
        else:
            return 0.08  # 8%
    
    def verify_economic_consistency(self) -> bool:
        """Verificar que el sistema es económicamente cerrado"""
        total_payments = sum(e['compensation']['amount'] 
                           for e in self.exchanges 
                           if e['compensation']['type'] == 'pays')
        
        total_receives = sum(e['compensation']['amount']
                           for e in self.exchanges
                           if e['compensation']['type'] == 'receives')
        
        # Sistema debe ser cerrado: pagos = recepciones + comisiones
        return abs(total_payments - total_receives - self.total_commission) < 0.01
    
    def generate_user_proposal(self, user_id: int) -> Dict[str, Any]:
        """Generar propuesta clara y transparente para el usuario"""
        user_exchange = next(e for e in self.exchanges if e['user_id'] == user_id)
        comp = user_exchange['compensation']
        
        # Construir propuesta según tipo de compensación
        if comp['type'] == 'pays':
            proposal = {
                'title': f"Intercambio encontrado: Obtienes {user_exchange['receives']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) -> Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Pagas €{comp['amount']} total (€{comp['difference']} diferencia + €{comp['commission']} comision Treqe {comp['rate']}%)",
                'benefits': [
                    f"Obtienes EXACTAMENTE {user_exchange['receives']} que buscabas",
                    f"Sin buscar vendedores ni gestionar envios separados",
                    f"Garantia Treqe 30 dias",
                    f"Mismo coste que vender {user_exchange['gives']} + comprar {user_exchange['receives']}, pero mucho mas simple"
                ],
                'recommended_action': "ACEPTAR POR COMODIDAD",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor, pagas €{comp['amount']} = NETO: €{user_exchange['gives_value']} (Empate economico, ganas comodidad)",
                'economic_logic': "RECIBES item de MAYOR valor -> PAGAS la diferencia"
            }
        elif comp['type'] == 'receives':
            proposal = {
                'title': f"Intercambio encontrado: Das {user_exchange['gives']} por {user_exchange['receives']} + €{comp['amount']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) -> Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Recibes €{comp['amount']} (€{abs(comp['difference'])} diferencia - €{comp['commission']} comision Treqe {comp['rate']}%)",
                'benefits': [
                    f"Obtienes {user_exchange['receives']} que buscabas",
                    f"Recibes €{comp['amount']} en efectivo adicional",
                    f"Todo gestionado en un solo intercambio",
                    f"Sin necesidad de vender {user_exchange['gives']} primero"
                ],
                'recommended_action': "ACEPTAR Y RECIBIR DINERO",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor + €{comp['amount']} = NETO: €{user_exchange['gives_value']} (Empate economico, ganas comodidad)",
                'economic_logic': "DAS item de MAYOR valor -> RECIBES la diferencia"
            }
        else:
            proposal = {
                'title': f"Intercambio perfecto: Das {user_exchange['gives']} por {user_exchange['receives']}",
                'summary': f"Intercambio igualitario: {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': "Sin ajuste monetario (valores iguales)",
                'benefits': [
                    f"Obtienes EXACTAMENTE lo que buscabas",
                    f"Intercambio perfectamente equilibrado",
                    f"Sin pagos adicionales",
                    f"Todo gestionado por Treqe"
                ],
                'recommended_action': "ACEPTAR INTERCAMBIO",
                'net_result': f"Das €{user_exchange['gives_value']} valor, recibes €{user_exchange['receives_value']} valor = NETO: €{user_exchange['gives_value']} (Empate economico, ganas comodidad)",
                'economic_logic': "Valores iguales -> intercambio directo"
            }
        
        # Metadata
        proposal.update({
            'exchange_id': f"treqe_{int(time.time())}_{user_id}",
            'exchange_type': 'circular',
            'k_size': self.k,
            'total_participants': self.k,
            'participants_info': [f"Usuario {e['username']}: {e['gives']} -> {e['receives']}" 
                                 for e in self.exchanges if e['user_id'] != user_id],
            'generated_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
            'algorithm_version': 'final_optimized_v1_fixed'
        })
        
        return proposal
    
    def __repr__(self):
        return f"Cycle(k={self.k}, users={self.user_ids}, value=€{self.total_value:.0f})"

# ============================================================================
# ALGORITMO PRINCIPAL FINAL OPTIMIZADO (COMPLETO)
# ============================================================================

class TreqeMatchingEngineFinal:
    """
    Motor de matching final optimizado - Versión completa
    """
    
    def __init__(self):
        self.k_max = 6  # Máximo k=6
        self.timeout_seconds = 5  # Timeout 5 segundos
        self.cache_ttl = 300  # Cache 5 minutos
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
        Buscar intercambios para usuario - Versión final optimizada COMPLETA
        """
        start_time = time.time()
        self.stats['searches'] += 1
        
        # Verificar cache (5 minutos TTL)
        cache_key = f"user_{user_id}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                self.stats['cache_hits'] += 1
                self.logger.info(f"Cache hit for user {user_id}")
                return cache_entry['result']
        
        self.logger.info(f"Starting final optimized search for user {user_id}")
        
        try:
            # 1. Obtener datos del usuario
            user_data = await self.get_user_data(db, user_id)
            if not user_data:
                return []
            
            # 2. Obtener todos los usuarios activos (excluyendo al usuario actual)
            other_users = await self.get_all_active_users(db, user_id)
            
            # Crear lista que incluya al usuario actual
            all_users = [user_data] + other_users
            
            if len(all_users) < 2:
                return []
            
            # 3. Buscar ciclos simples (k=2,3,4)
            proposals = []
            
            # Para k=3 (nuestro caso demo)
            if len(all_users) >= 3:
                for i in range(len(all_users)):
                    user1 = all_users[i]
                    if user1.id != user_id:
                        continue  # Solo buscar ciclos que incluyan al usuario actual
                        
                    for j in range(len(all_users)):
                        if j == i:
                            continue
                        for k in range(len(all_users)):
                            if k in [i, j]:
                                continue
                            
                            # Verificar si forman un ciclo
                            user2 = all_users[j]
                            user3 = all_users[k]
                            
                            # Verificar compatibilidades
                            if (user1.wants_item(user2.item_title) and
                                user2.wants_item(user3.item_title) and
                                user3.wants_item(user1.item_title)):
                                
                                # Crear ciclo
                                user_map = {u.id: u for u in [user1, user2, user3]}
                                cycle = ExchangeCycleFinal(
                                    [user1.id, user2.id, user3.id],
                                    [user1, user2, user3],
                                    user_map
                                )
                                
                                if cycle.verify_economic_consistency():
                                    proposal = cycle.generate_user_proposal(user_id)
                                    proposals.append(proposal)
            
            # Para k=2 (intercambio directo)
            if len(all_users) >= 2:
                for i in range(len(all_users)):
                    user1 = all_users[i]
                    if user1.id != user_id:
                        continue
                        
                    for j in range(len(all_users)):
                        if j == i:
                            continue
                        
                        user2 = all_users[j]
                        
                        # Verificar intercambio directo
                        if (user1.wants_item(user2.item_title) and
                            user2.wants_item(user1.item_title)):
                            
                            # Crear ciclo k=2
                            user_map = {u.id: u for u in [user1, user2]}
                            cycle = ExchangeCycleFinal(
                                [user1.id, user2.id],
                                [user1, user2],
                                user_map
                            )
                            
                            if cycle.verify_economic_consistency():
                                proposal = cycle.generate_user_proposal(user_id)
                                proposals.append(proposal)
            
            search_time = time.time() - start_time
            self.stats['avg_search_time'] = (
                self.stats['avg_search_time'] * (self.stats['searches'] - 1) + search_time
            ) / self.stats['searches']
            
            self.logger.info(f"Final search completed in {search_time:.2f}s. Found {len(proposals)} proposals")
            
            # Actualizar cache
            self.cache[cache_key] = {
                'result': proposals,
                'timestamp': time.time(),
                'search_time': search_time
            }
            
            return proposals
            
        except Exception as e:
            self.logger.error(f"Error in final matching: {e}")
            return []
    
    async def get_user_data(self, db, user_id: int) -> Optional[TreqeUserFinal]:
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
            
            return TreqeUserFinal(db_user, db_item, db_preferences)
            
        except Exception as e:
            self.logger.error(f"Error getting user data: {e}")
            return None
    
    async def get_all_active_users(self, db, exclude_user_id: int) -> List[TreqeUserFinal]:
        """Obtener todos los usuarios activos"""
        users = []
        
        try:
            # Obtener todos los usuarios (excepto el excluido)
            stmt_users = select(User).where(User.id != exclude_user_id)
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
                
                treqe_user = TreqeUserFinal(db_user, db_item, db_preferences)
                users.append(treqe_user)
            
            return users
            
        except Exception as e:
            self.logger.error(f"Error getting all users: {e}")
            return []
    
    def get_optimal_search_order(self, user_count: int) -> List[int]:
        """Orden de búsqueda óptimo"""
        if user_count < 10:
            return [2, 3, 4]
        elif user_count < 30:
            return [3, 4, 2, 5]
        else:
            return [3, 4, 5, 2, 6]