"""
Algoritmo Treqe Simple - Versión MVP
Lógica de matching simple para validación rápida
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

logger = get_logger("core.algorithm_simple")

# ============================================================================
# LÓGICA SIMPLE DE MATCHING
# ============================================================================

class TreqeUserSimple:
    """Usuario simple para algoritmo MVP"""
    __slots__ = ['id', 'username', 'reputation', 'item_id', 'item_title', 
                 'item_value', 'desired_titles', 'min_value', 'max_value']
    
    def __init__(self, db_user: User, db_item: Item, db_preferences: List[Preference]):
        self.id = db_user.id
        self.username = db_user.username
        self.reputation = float(db_user.reputation_score)
        
        self.item_id = db_item.id
        self.item_title = db_item.title
        self.item_value = float(db_item.estimated_value)
        
        # Preferencias simplificadas
        self.desired_titles = []
        self.min_value = float('inf')
        self.max_value = 0
        
        for pref in db_preferences:
            if pref.is_active:
                self.desired_titles.append(pref.desired_item_title.lower())
                self.min_value = min(self.min_value, float(pref.min_value))
                self.max_value = max(self.max_value, float(pref.max_value))
    
    def wants_item(self, item_title: str, item_value: float) -> bool:
        """Verificación simple de compatibilidad"""
        item_title_lower = item_title.lower()
        
        # Para cada título deseado
        for desired in self.desired_titles:
            # Verificar si el título del item contiene palabras clave del deseado
            desired_words = set(re.findall(r'\w+', desired))
            item_words = set(re.findall(r'\w+', item_title_lower))
            
            # Si hay al menos 2 palabras en común
            common_words = desired_words & item_words
            if len(common_words) >= 2:
                # Verificar rango de valor
                if self.min_value <= item_value <= self.max_value:
                    return True
        
        return False
    
    def __repr__(self):
        return f"User{self.id}:{self.item_title[:15]}...€{self.item_value}"

class ExchangeCycleSimple:
    """Ciclo de intercambio simple"""
    def __init__(self, user_ids: List[int], users: List[TreqeUserSimple]):
        self.user_ids = user_ids
        self.k = len(user_ids)
        self.exchanges = []
        self.total_value = 0
        self.total_commission = 0
        
        user_map = {user.id: user for user in users}
        
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
            
            # Lógica económica
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
        """Generar propuesta simple"""
        user_exchange = next(e for e in self.exchanges if e['user_id'] == user_id)
        comp = user_exchange['compensation']
        
        if comp['type'] == 'pays':
            proposal = {
                'title': f"Intercambio encontrado: Obtienes {user_exchange['receives']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) -> Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Pagas €{comp['amount']} total (€{comp['difference']} diferencia + €{comp['commission']} comision Treqe {comp['rate']}%)",
                'economic_logic': "RECIBES item de MAYOR valor -> PAGAS la diferencia"
            }
        elif comp['type'] == 'receives':
            proposal = {
                'title': f"Intercambio encontrado: Das {user_exchange['gives']} por {user_exchange['receives']} + €{comp['amount']}",
                'summary': f"Das {user_exchange['gives']} (€{user_exchange['gives_value']}) -> Recibes {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': f"Recibes €{comp['amount']} (€{abs(comp['difference'])} diferencia - €{comp['commission']} comision Treqe {comp['rate']}%)",
                'economic_logic': "DAS item de MAYOR valor -> RECIBES la diferencia"
            }
        else:
            proposal = {
                'title': f"Intercambio perfecto: Das {user_exchange['gives']} por {user_exchange['receives']}",
                'summary': f"Intercambio igualitario: {user_exchange['gives']} (€{user_exchange['gives_value']}) por {user_exchange['receives']} (€{user_exchange['receives_value']})",
                'financial_adjustment': "Sin ajuste monetario (valores iguales)",
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
            'algorithm_version': 'simple_v1'
        })
        
        return proposal

# ============================================================================
# ALGORITMO SIMPLE
# ============================================================================

class TreqeMatchingEngineSimple:
    """Motor de matching simple para MVP"""
    
    def __init__(self):
        self.k_max = 6
        self.timeout_seconds = 5
        self.logger = get_logger("core.algorithm_simple")
    
    async def get_user_data(self, db, user_id: int) -> Optional[TreqeUserSimple]:
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
            
            return TreqeUserSimple(db_user, db_item, db_preferences)
            
        except Exception as e:
            self.logger.error(f"Error getting user data: {e}")
            return None
    
    async def find_exchanges_for_user(self, db, user_id: int) -> List[Dict[str, Any]]:
        """Buscar intercambios para usuario (versión simple)"""
        start_time = time.time()
        
        try:
            # Obtener datos del usuario
            user_data = await self.get_user_data(db, user_id)
            if not user_data:
                return []
            
            # Obtener todos los usuarios activos
            stmt_users = select(User).where(User.id != user_id)
            result_users = await db.execute(stmt_users)
            db_users = result_users.scalars().all()
            
            # Convertir a TreqeUserSimple
            all_treqe_users = [user_data]
            
            for db_user in db_users:
                # Obtener item
                stmt_item = select(Item).where(
                    Item.user_id == db_user.id,
                    Item.status == "available"
                )
                result_item = await db.execute(stmt_item)
                db_item = result_item.scalar_one_or_none()
                
                if not db_item:
                    continue
                
                # Obtener preferencias
                stmt_prefs = select(Preference).where(
                    Preference.user_id == db_user.id,
                    Preference.is_active == True
                )
                result_prefs = await db.execute(stmt_prefs)
                db_preferences = result_prefs.scalars().all()
                
                if not db_preferences:
                    continue
                
                treqe_user = TreqeUserSimple(db_user, db_item, db_preferences)
                all_treqe_users.append(treqe_user)
            
            # Buscar ciclos simples (k=2,3,4)
            proposals = []
            
            # Para k=3 (nuestro caso demo)
            if len(all_treqe_users) >= 3:
                # Probar todas las combinaciones de 3 usuarios
                for i in range(len(all_treqe_users)):
                    for j in range(len(all_treqe_users)):
                        if j == i:
                            continue
                        for k in range(len(all_treqe_users)):
                            if k in [i, j]:
                                continue
                            
                            # Verificar si forman un ciclo
                            user1 = all_treqe_users[i]
                            user2 = all_treqe_users[j]
                            user3 = all_treqe_users[k]
                            
                            # Verificar compatibilidades
                            if (user1.wants_item(user2.item_title, user2.item_value) and
                                user2.wants_item(user3.item_title, user3.item_value) and
                                user3.wants_item(user1.item_title, user1.item_value)):
                                
                                # Crear ciclo
                                cycle = ExchangeCycleSimple(
                                    [user1.id, user2.id, user3.id],
                                    [user1, user2, user3]
                                )
                                
                                if cycle.verify_economic_consistency():
                                    proposal = cycle.generate_user_proposal(user_id)
                                    proposals.append(proposal)
            
            # Para k=2 (intercambio directo)
            if len(all_treqe_users) >= 2:
                for i in range(len(all_treqe_users)):
                    user1 = all_treqe_users[i]
                    if user1.id != user_id:
                        continue
                        
                    for j in range(len(all_treqe_users)):
                        if j == i:
                            continue
                        
                        user2 = all_treqe_users[j]
                        
                        # Verificar intercambio directo
                        if (user1.wants_item(user2.item_title, user2.item_value) and
                            user2.wants_item(user1.item_title, user1.item_value)):
                            
                            # Crear ciclo k=2
                            cycle = ExchangeCycleSimple(
                                [user1.id, user2.id],
                                [user1, user2]
                            )
                            
                            if cycle.verify_economic_consistency():
                                proposal = cycle.generate_user_proposal(user_id)
                                proposals.append(proposal)
            
            search_time = time.time() - start_time
            self.logger.info(f"Simple search completed in {search_time:.2f}s. Found {len(proposals)} proposals")
            
            return proposals
            
        except Exception as e:
            self.logger.error(f"Error in simple matching: {e}")
            return []