"""
Motor de matching Treqe - Versión simplificada para MVP
"""

import time
from typing import List, Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database.models import User, Item, Preference
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("core.matching")

class TreqeMatchingEngine:
    """Motor de matching simplificado para MVP"""
    
    def __init__(self):
        self.timeout_seconds = settings.TREQE_TIMEOUT_SECONDS
        self.k_max = settings.TREQE_K_MAX
    
    async def find_exchanges_for_user(self, db: AsyncSession, user_id: int) -> List[Dict[str, Any]]:
        """
        Encontrar intercambios para un usuario específico
        Versión simplificada para MVP
        """
        start_time = time.time()
        logger.info(f"Finding exchanges for user {user_id}")
        
        # 1. Obtener datos del usuario
        user_data = await self.get_user_data(db, user_id)
        if not user_data:
            logger.warning(f"User {user_id} has no active items or preferences")
            return []
        
        # 2. Buscar intercambios simples (k=2 primero)
        exchanges = []
        
        # Buscar intercambios directos (k=2)
        direct_exchanges = await self.find_direct_exchanges(db, user_data)
        exchanges.extend(direct_exchanges)
        
        # Si no hay intercambios directos, buscar ciclos k=3
        if not exchanges:
            cycle_exchanges = await self.find_cycle_exchanges(db, user_data)
            exchanges.extend(cycle_exchanges)
        
        search_time = time.time() - start_time
        logger.info(f"Search completed in {search_time:.2f}s. Found {len(exchanges)} exchanges")
        
        return exchanges
    
    async def get_user_data(self, db: AsyncSession, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtener datos del usuario"""
        # Obtener usuario
        stmt_user = select(User).where(User.id == user_id, User.is_active == True)
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
        
        return {
            'user': db_user,
            'item': db_item,
            'preferences': db_preferences
        }
    
    async def find_direct_exchanges(self, db: AsyncSession, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Buscar intercambios directos (k=2)"""
        exchanges = []
        user = user_data['user']
        user_item = user_data['item']
        user_preferences = user_data['preferences']
        
        # Para cada preferencia del usuario
        for pref in user_preferences:
            # Buscar usuarios que tengan el item deseado
            stmt_target_users = select(User).join(Item).where(
                User.is_active == True,
                User.id != user.id,
                Item.status == "available",
                Item.title.ilike(f"%{pref.desired_item_title}%")
            ).limit(10)
            
            result_targets = await db.execute(stmt_target_users)
            target_users = result_targets.scalars().all()
            
            for target_user in target_users:
                # Verificar si el usuario objetivo quiere el item del usuario
                stmt_target_prefs = select(Preference).where(
                    Preference.user_id == target_user.id,
                    Preference.is_active == True,
                    Preference.desired_item_title.ilike(f"%{user_item.title}%")
                )
                result_target_prefs = await db.execute(stmt_target_prefs)
                target_prefs = result_target_prefs.scalars().all()
                
                if target_prefs:
                    # ¡Encontramos un intercambio directo!
                    exchange = await self.create_direct_exchange(
                        db, user, user_item, target_user, pref, target_prefs[0]
                    )
                    if exchange:
                        exchanges.append(exchange)
        
        return exchanges
    
    async def create_direct_exchange(self, db: AsyncSession, user1: User, item1: Item,
                                   user2: User, pref1: Preference, pref2: Preference) -> Optional[Dict[str, Any]]:
        """Crear propuesta de intercambio directo"""
        # Obtener item de user2
        stmt_item2 = select(Item).where(
            Item.user_id == user2.id,
            Item.status == "available",
            Item.title.ilike(f"%{pref1.desired_item_title}%")
        )
        result_item2 = await db.execute(stmt_item2)
        item2 = result_item2.scalar_one_or_none()
        
        if not item2:
            return None
        
        # Calcular compensaciones económicas
        value1 = float(item1.estimated_value)
        value2 = float(item2.estimated_value)
        difference = value2 - value1
        
        # Comisiones según reputación
        commission_rate1 = self.get_commission_rate(user1.reputation_score)
        commission_rate2 = self.get_commission_rate(user2.reputation_score)
        
        if difference > 0:
            # User1 recibe item de mayor valor → paga diferencia
            commission1 = difference * commission_rate1
            payment1 = difference + commission1
            
            compensation1 = {
                'type': 'pays',
                'amount': payment1,
                'difference': difference,
                'commission': commission1,
                'rate': commission_rate1 * 100
            }
            compensation2 = {
                'type': 'receives',
                'amount': difference - commission1,  # User2 recibe diferencia menos comisión Treqe
                'difference': -difference,
                'commission': 0,
                'rate': 0
            }
        elif difference < 0:
            # User2 recibe item de mayor valor → paga diferencia
            commission2 = abs(difference) * commission_rate2
            payment2 = abs(difference) + commission2
            
            compensation1 = {
                'type': 'receives',
                'amount': abs(difference) - commission2,
                'difference': difference,
                'commission': 0,
                'rate': 0
            }
            compensation2 = {
                'type': 'pays',
                'amount': payment2,
                'difference': -difference,
                'commission': commission2,
                'rate': commission_rate2 * 100
            }
        else:
            # Valores iguales
            compensation1 = {
                'type': 'equal',
                'amount': 0,
                'difference': 0,
                'commission': 0,
                'rate': 0
            }
            compensation2 = compensation1.copy()
        
        # Crear propuesta
        proposal = {
            'exchange_type': 'direct',
            'k_size': 2,
            'participants': [
                {
                    'user_id': user1.id,
                    'username': user1.username,
                    'gives_item': {
                        'id': item1.id,
                        'title': item1.title,
                        'value': value1
                    },
                    'receives_item': {
                        'id': item2.id,
                        'title': item2.title,
                        'value': value2
                    },
                    'compensation': compensation1
                },
                {
                    'user_id': user2.id,
                    'username': user2.username,
                    'gives_item': {
                        'id': item2.id,
                        'title': item2.title,
                        'value': value2
                    },
                    'receives_item': {
                        'id': item1.id,
                        'title': item1.title,
                        'value': value1
                    },
                    'compensation': compensation2
                }
            ],
            'total_value': value1 + value2,
            'total_commission': compensation1.get('commission', 0) + compensation2.get('commission', 0)
        }
        
        # Generar propuesta para user1
        user1_proposal = self.generate_user_proposal(proposal, user1.id)
        
        return user1_proposal
    
    async def find_cycle_exchanges(self, db: AsyncSession, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Buscar intercambios en ciclo (k=3) - Versión simplificada"""
        # Para MVP, usaremos un ejemplo predefinido
        # En producción, esto buscaría ciclos reales
        
        exchanges = []
        
        # Ejemplo de ciclo k=3 (como el que usamos en la demostración)
        example_cycle = await self.create_example_cycle(db, user_data)
        if example_cycle:
            exchanges.append(example_cycle)
        
        return exchanges
    
    async def create_example_cycle(self, db: AsyncSession, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crear ejemplo de ciclo k=3 para demostración"""
        user = user_data['user']
        user_item = user_data['item']
        
        # Crear usuarios de ejemplo
        example_users = [
            {
                'username': 'Carlos',
                'item_title': 'MacBook Air M1',
                'item_value': 800.0,
                'wants': 'Bicicleta carretera'
            },
            {
                'username': 'Beatriz',
                'item_title': 'Bicicleta carretera',
                'item_value': 400.0,
                'wants': 'iPhone 13'
            }
        ]
        
        # Verificar que el usuario tenga un iPhone (para el ejemplo)
        if 'iPhone' not in user_item.title and 'iphone' not in user_item.title.lower():
            return None
        
        # Crear propuesta de ciclo
        proposal = {
            'exchange_type': 'cycle',
            'k_size': 3,
            'participants': [
                {
                    'user_id': user.id,
                    'username': user.username,
                    'gives_item': {
                        'id': user_item.id,
                        'title': user_item.title,
                        'value': float(user_item.estimated_value)
                    },
                    'receives_item': {
                        'id': 9991,  # ID ficticio
                        'title': 'MacBook Air M1',
                        'value': 800.0
                    },
                    'compensation': {
                        'type': 'pays',
                        'amount': 212.0,
                        'difference': 200.0,
                        'commission': 12.0,
                        'rate': 6.0
                    }
                },
                {
                    'user_id': 9992,  # ID ficticio
                    'username': 'Carlos',
                    'gives_item': {
                        'id': 9993,
                        'title': 'MacBook Air M1',
                        'value': 800.0
                    },
                    'receives_item': {
                        'id': 9994,
                        'title': 'Bicicleta carretera',
                        'value': 400.0
                    },
                    'compensation': {
                        'type': 'receives',
                        'amount': 376.0,
                        'difference': -400.0,
                        'commission': 24.0,
                        'rate': 6.0
                    }
                },
                {
                    'user_id': 9995,  # ID ficticio
                    'username': 'Beatriz',
                    'gives_item': {
                        'id': 9996,
                        'title': 'Bicicleta carretera',
                        'value': 400.0
                    },
                    'receives_item': {
                        'id': user_item.id,
                        'title': user_item.title,
                        'value': float(user_item.estimated_value)
                    },
                    'compensation': {
                        'type': 'pays',
                        'amount': 212.0,
                        'difference': 200.0,
                        'commission': 12.0,
                        'rate': 6.0
                    }
                }
            ],
            'total_value': float(user_item.estimated_value) + 800.0 + 400.0,
            'total_commission': 48.0,
            'is_example': True
        }
        
        # Generar propuesta para el usuario
        user_proposal = self.generate_user_proposal(proposal, user.id)
        user_proposal['is_example'] = True
        user_proposal['note'] = "This is a demonstration cycle. In production, real users would be matched."
        
        return user_proposal
    
    def generate_user_proposal(self, exchange: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """Generar propuesta para un usuario específico"""
        # Encontrar los datos del usuario en el intercambio
        user_data = None
        other_participants = []
        
        for participant in exchange['participants']:
            if participant['user_id'] == user_id:
                user_data = participant
            else:
                other_participants.append({
                    'username': participant['username'],
                    'exchange': f"{participant['gives_item']['title']} → {participant['receives_item']['title']}"
                })
        
        if not user_data:
            return None
        
        # Construir propuesta según tipo de compensación
        compensation = user_data['compensation']
        
        if compensation['type'] == 'pays':
            proposal = {
                'title': f"Exchange found: You get {user_data['receives_item']['title']}",
                'summary': f"You give {user_data['gives_item']['title']} (€{user_data['gives_item']['value']}) for {user_data['receives_item']['title']} (€{user_data['receives_item']['value']})",
                'financial_adjustment': f"Pay €{compensation['amount']:.2f} total (€{compensation['difference']:.2f} difference + €{compensation['commission']:.2f} Treqe commission)",
                'benefits': [
                    f"You get EXACTLY {user_data['receives_item']['title']} that you wanted",
                    f"No need to search for sellers or manage separate shipments",
                    f"Treqe 30-day guarantee",
                    f"Same cost as selling {user_data['gives_item']['title']} + buying {user_data['receives_item']['title']}, but much simpler"
                ],
                'recommended_action': "ACCEPT FOR CONVENIENCE",
                'net_result': f"You give €{user_data['gives_item']['value']} value, receive €{user_data['receives_item']['value']} value, pay €{compensation['amount']:.2f} = NET: €{user_data['gives_item']['value']} (Economic tie, you gain convenience)"
            }
        elif compensation['type'] == 'receives':
            proposal = {
                'title': f"Exchange found: You give {user_data['gives_item']['title']} for {user_data['receives_item']['title']} + €{compensation['amount']:.2f}",
                'summary': f"You give {user_data['gives_item']['title']} (€{user_data['gives_item']['value']}) for {user_data['receives_item']['title']} (€{user_data['receives_item']['value']})",
                'financial_adjustment': f"Receive €{compensation['amount']:.2f} (€{abs(compensation['difference']):.2f} difference - €{compensation['commission']:.2f} Treqe commission)",
                'benefits': [
                    f"You get {user_data['receives_item']['title']} that you wanted",
                    f"You receive €{compensation['amount']:.2f} in cash",
                    f"Everything managed in a single exchange",
                    f"No need to sell {user_data['gives_item']['title']} first"
                ],
                'recommended_action': "ACCEPT AND RECEIVE MONEY",
                'net_result': f"You give €{user_data['gives_item']['value']} value, receive €{user_data['receives_item']['value']} value + €{compensation['amount']:.2f} = NET: €{user_data['gives_item']['value']} (Economic tie, you gain convenience)"
            }
        else:
            proposal = {
                'title': f"Perfect exchange: You give {user_data['gives_item']['title']} for {user_data['receives_item']['title']}",
                'summary': f"Equal exchange: {user_data['gives_item']['title']} (€{user_data['gives_item']['value']}) for {user_data['receives_item']['title']} (€{user_data['receives_item']['value']})",
                'financial_adjustment': "No monetary adjustment (equal values)",
                'benefits': [
                    f"You get EXACTLY what you wanted",
                    f"Perfectly balanced exchange",
                    f"No additional payments",
                    f"Everything managed by Treqe"
                ],
                'recommended_action': "ACCEPT EXCHANGE",
                'net_result': f"You give €{user_data['gives_item']['value']} value, receive €{user_data['receives_item']['value']} value = NET: €{user_data['gives_item']['value']} (Economic tie, you gain convenience)"
            }
        
        # Añadir metadata
        proposal.update({
            'exchange_id': f"exch_{int(time.time())}_{user_id}",
            'exchange_type': exchange['exchange_type'],
            'k_size': exchange['k_size'],
            'other_participants': other_participants,
            'total_participants': exchange['k_size'],
            'generated_at': time.time(),
            'expires_at': time.time() + (24 * 3600)  # Expira en 24 horas
        })
        
        return proposal
    
    def get_commission_rate(self, reputation_score: float) -> float:
        """Obtener tasa de comisión según reputación"""
        if reputation_score >= 80:
            return settings.COMMISSION_RATE_HIGH
        elif reputation_score >= 60:
            return settings.COMMISSION_RATE_MEDIUM
        else:
            return settings.COMMISSION_RATE_LOW

# Instancia global del motor de matching
matching_engine = TreqeMatchingEngine()