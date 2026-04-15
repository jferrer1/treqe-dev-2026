"""
Algoritmo de matching Treqe - Lógica económica correcta
Integración del algoritmo corregido en el backend
"""

import time
import random
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict
from datetime import datetime, timedelta

from ..database.models import User, Item, Preference
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("core.algorithm")

# ============================================================================
# CLASES PARA EL ALGORITMO
# ============================================================================

class TreqeUser:
    """Usuario para el algoritmo de matching"""
    def __init__(self, db_user: User, db_item: Item, db_preferences: List[Preference]):
        self.id = db_user.id
        self.username = db_user.username
        self.reputation = float(db_user.reputation_score)
        
        self.item_id = db_item.id
        self.item_title = db_item.title
        self.item_value = float(db_item.estimated_value)
        
        # Preferencias activas
        self.desired_items = []
        self.desired_values = []
        
        for pref in db_preferences:
            if pref.is_active:
                self.desired_items.append(pref.desired_item_title)
                # Usar el valor del item ofrecido como referencia para valor deseado
                self.desired_values.append(self.item_value * random.uniform(0.8, 1.2))
    
    def __repr__(self):
        return f"TreqeUser({self.id}: {self.item_title}€{self.item_value} -> {self.desired_items})"

class ExchangeCycle:
    """Ciclo de intercambio con compensaciones económicas correctas"""
    def __init__(self, user_ids: List[int], users: List[TreqeUser], db_users: Dict[int, User]):
        self.user_ids = user_ids
        self.k = len(user_ids)
        self.users = {u.id: u for u in users}
        self.db_users = db_users
        self.exchanges = []
        self.compensations = {}
        self.calculate_exchanges()
    
    def calculate_exchanges(self):
        """Determinar qué recibe cada usuario y calcular compensaciones"""
        # Paso 1: Determinar flujo de items
        for i in range(self.k):
            id_from = self.user_ids[i]
            id_to = self.user_ids[(i + 1) % self.k]
            
            user_from = self.users[id_from]
            user_to = self.users[id_to]
            
            # Encontrar qué item quiere 'from' de 'to'
            item_receives = user_to.item_title
            value_receives = user_to.item_value
            
            self.exchanges.append({
                'user_id': id_from,
                'username': user_from.username,
                'gives': user_from.item_title,
                'gives_value': user_from.item_value,
                'receives': item_receives,
                'receives_value': value_receives,
                'from_user_id': id_to,
                'from_username': user_to.username
            })
        
        # Paso 2: Calcular compensaciones (regla CORRECTA)
        for exchange in self.exchanges:
            user_id = exchange['user_id']
            gives_value = exchange['gives_value']
            receives_value = exchange['receives_value']
            
            difference = receives_value - gives_value  # Positiva si recibe más valor
            
            # Comisión Treqe según reputación
            db_user = self.db_users.get(user_id)
            reputation = db_user.reputation_score if db_user else 50.0
            
            commission_rate = settings.COMMISSION_RATE_LOW
            if reputation >= 80:
                commission_rate = settings.COMMISSION_RATE_HIGH
            elif reputation >= 60:
                commission_rate = settings.COMMISSION_RATE_MEDIUM
            
            if difference > 0:
                # Recibe item de MAYOR valor → PAGA diferencia + comisión
                commission = difference * commission_rate
                total_payment = difference + commission
                
                self.compensations[user_id] = {
                    'type': 'pays',
                    'amount': total_payment,
                    'value_difference': difference,
                    'commission': commission,
                    'commission_rate': commission_rate * 100,
                    'reason': f"Receives {exchange['receives']} (€{receives_value}) worth €{difference} more than {exchange['gives']} (€{gives_value})"
                }
            elif difference < 0:
                # Da item de MAYOR valor → RECIBE diferencia - comisión
                commission = abs(difference) * commission_rate
                total_receives = abs(difference) - commission
                
                self.compensations[user_id] = {
                    'type': 'receives',
                    'amount': total_receives,
                    'value_difference': difference,
                    'commission': commission,
                    'commission_rate': commission_rate * 100,
                    'reason': f"Gives {exchange['gives']} (€{gives_value}) worth €{abs(difference)} more than receives {exchange['receives']} (€{receives_value})"
                }
            else:
                # Valores iguales
                self.compensations[user_id] = {
                    'type': 'equal',
                    'amount': 0,
                    'value_difference': 0,
                    'commission': 0,
                    'commission_rate': 0,
                    'reason': "Equal value exchange"
                }
    
    def verify_economic_consistency(self) -> bool:
        """Verificar que el sistema económico sea consistente"""
        total_payments = 0
        total_receives = 0
        total_commissions = 0
        
        for comp in self.compensations.values():
            if comp['type'] == 'pays':
                total_payments += comp['amount']
            elif comp['type'] == 'receives':
                total_receives += comp['amount']
            total_commissions += comp['commission']
        
        # En un sistema cerrado: pagos = recibos + comisiones
        return abs(total_payments - total_receives - total_commissions) < 0.01
    
    def generate_user_proposal(self, user_id: int) -> Dict[str, Any]:
        """Generar propuesta para un usuario específico"""
        if user_id not in self.users:
            return None
        
        # Encontrar intercambio de este usuario
        user_exchange = None
        for exchange in self.exchanges:
            if exchange['user_id'] == user_id:
                user_exchange = exchange
                break
        
        if not user_exchange:
            return None
        
        compensation = self.compensations.get(user_id, {'type': 'equal', 'amount': 0})
        
        # Construir propuesta
        if compensation['type'] == 'pays':
            proposal = {
                'title': f"Exchange found: You get {user_exchange['receives']}",
                'summary': f"You give {user_exchange['gives']} (€{user_exchange['gives_value']}) for {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Pay €{compensation['amount']:.2f} total (€{compensation['value_difference']:.2f} difference + €{compensation['commission']:.2f} Treqe commission)",
                'benefits': [
                    f"You get EXACTLY {user_exchange['receives']} that you wanted",
                    f"No need to search for sellers or manage separate shipments",
                    f"Treqe 30-day guarantee",
                    f"Same cost as selling {user_exchange['gives']} + buying {user_exchange['receives']}, but much simpler"
                ],
                'recommended_action': "ACCEPT FOR CONVENIENCE",
                'net_result': f"You give €{user_exchange['gives_value']} value, receive €{user_exchange['receives_value']} value, pay €{compensation['amount']:.2f} = NET: €{user_exchange['gives_value']} (Economic tie, you gain convenience)"
            }
        elif compensation['type'] == 'receives':
            proposal = {
                'title': f"Exchange found: You give {user_exchange['gives']} for {user_exchange['receives']} + €{compensation['amount']:.2f}",
                'summary': f"You give {user_exchange['gives']} (€{user_exchange['gives_value']}) for {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Receive €{compensation['amount']:.2f} (€{abs(compensation['value_difference']):.2f} difference - €{compensation['commission']:.2f} Treqe commission)",
                'benefits': [
                    f"You get {user_exchange['receives']} that you wanted",
                    f"You receive €{compensation['amount']:.2f} in cash",
                    f"Everything managed in a single exchange",
                    f"No need to sell {user_exchange['gives']} first"
                ],
                'recommended_action': "ACCEPT AND RECEIVE MONEY",
                'net_result': f"You give €{user_exchange['gives_value']} value, receive €{user_exchange['receives_value']} value + €{compensation['amount']:.2f} = NET: €{user_exchange['gives_value']} (Economic tie, you gain convenience)"
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
        
        # Información sobre otros participantes (anonimizada)
        other_participants = []
        for exchange in self.exchanges:
            if exchange['user_id'] != user_id:
                other_participants.append(f"User exchanges {exchange['gives']} for {exchange['receives']}")
        
        proposal['other_participants'] = other_participants
        proposal['total_participants'] = self.k
        proposal['generated_at'] = datetime.now().isoformat()
        
        return proposal
    
    def __repr__(self):
        return f"ExchangeCycle(k={self.k}, users={self.user_ids})"

# ============================================================================
# ALGORITMO PRINCIPAL
# ============================================================================

class TreqeMatchingEngine:
    """Motor de matching para Treqe"""
    
    def __init__(self, timeout_seconds: int = None, k_max: int = None):
        self.timeout_seconds = timeout_seconds or settings.TREQE_TIMEOUT_SECONDS
        self.k_max = k_max or settings.TREQE_K_MAX
        self.logger = get_logger("core.matching")
    
    async def find_exchanges_for_user(self, db, user_id: int) -> List[ExchangeCycle]:
        """
        Encontrar intercambios para un usuario específico
        """
        start_time = time.time()
        self.logger.info(f"Finding exchanges for user {user_id}")
        
        # 1. Obtener datos del usuario
        user_data = await self.get_user_data(db, user_id)
        if not user_data:
            self.logger.warning(f"User {user_id} has no active items or preferences")
            return []
        
        # 2. Obtener pool de usuarios compatibles
        compatible_users = await self.get_compatible_users_pool(db, user_data)
        self.logger.info(f"Found {len(compatible_users)} compatible users in pool")
        
        if len(compatible_users) < 2:  # Necesitamos al menos otro usuario
            self.logger.info(f"Insufficient compatible users for matching")
            return []
        
        # 3. Construir grafo de preferencias
        graph = self.build_preference_graph(compatible_users)
        
        # 4. Buscar ciclos ascendente (k=2 → k_max)
        found_cycles = []
        matched_user_ids = set()
        
        for k in range(2, self.k_max + 1):
            if time.time() - start_time > self.timeout_seconds:
                self.logger.warning(f"Timeout reached after {self.timeout_seconds}s")
                break
            
            if len(compatible_users) - len(matched_user_ids) < k:
                break
            
            self.logger.debug(f"Searching for cycles of size k={k}")
            cycles = self.find_cycles_of_size_k(graph, k, matched_user_ids, start_time)
            
            if cycles:
                # Procesar el primer ciclo encontrado
                cycle_ids = cycles[0]
                try:
                    cycle_users = [u for u in compatible_users if u.id in cycle_ids]
                    db_users_map = {u.id: u for u in compatible_users}
                    
                    cycle = ExchangeCycle(list(cycle_ids), cycle_users, db_users_map)
                    
                    if cycle.verify_economic_consistency():
                        found_cycles.append(cycle)
                        matched_user_ids.update(cycle_ids)
                        self.logger.info(f"Found valid cycle k={k}: {cycle}")
                    else:
                        self.logger.warning(f"Cycle failed economic consistency check: {cycle_ids}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing cycle: {e}")
                    continue
        
        search_time = time.time() - start_time
        self.logger.info(f"Search completed in {search_time:.2f}s. Found {len(found_cycles)} cycles")
        
        return found_cycles
    
    async def get_user_data(self, db, user_id: int) -> Optional[TreqeUser]:
        """Obtener datos del usuario para el algoritmo"""
        from sqlalchemy import select
        
        # Obtener usuario con item activo
        stmt_user = select(User).where(User.id == user_id, User.is_active == True)
        result_user = await db.execute(stmt_user)
        db_user = result_user.scalar_one_or_none()
        
        if not db_user:
            return None
        
        # Obtener item activo del usuario
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
        
        return TreqeUser(db_user, db_item, db_preferences)
    
    async def get_compatible_users_pool(self, db, target_user: TreqeUser) -> List[TreqeUser]:
        """Obtener pool de usuarios compatibles"""
        from sqlalchemy import select
        
        compatible_users = [target_user]
        
        # Obtener todos los usuarios activos con items disponibles
        stmt_users = select(User).where(
            User.is_active == True,
            User.id != target_user.id
        ).limit(100)  # Limitar para performance
        
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
            
            # Verificar compatibilidad básica
            treqe_user = TreqeUser(db_user, db_item, db_preferences)
            
            # Verificar si el item de este usuario está en las preferencias del usuario objetivo
            # o viceversa (simplificado para MVP)
            if self.are_users_compatible(target_user, treqe_user):
                compatible_users.append(treqe_user)
        
        return compatible_users
    
    def are_users_compatible(self, user1: TreqeUser, user2: TreqeUser) -> bool:
        """Verificar compatibilidad básica entre dos usuarios"""
        # User1 quiere lo que tiene User2
        user1_wants_user2 = any(
            user2.item_title.lower() in item.lower() or item.lower() in user2.item_title.lower()
            for item in user1.desired_items
        )
        
        # User2 quiere lo que tiene User1
        user2_wants_user1 = any(
            user1.item_title.lower() in item.lower() or item.lower() in user1.item_title.lower()
            for item in user2.desired_items
        )
        
        return user1_wants_user2 or user2_w