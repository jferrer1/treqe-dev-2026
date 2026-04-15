"""
Endpoints API para gestión de propuestas de intercambio
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
import time

from .auth import CurrentUser
from ..database.connection import get_db
from ..database.models import User, Exchange, ExchangeParticipant, Item
from ..utils.logger import get_logger

logger = get_logger("api.proposals")

router = APIRouter()

# Almacenamiento temporal de propuestas (para MVP)
# En producción, esto estaría en base de datos o Redis
proposal_store = {}

@router.get("/", response_model=List[dict])
async def list_proposals(
    current_user: User = CurrentUser,
    status_filter: Optional[str] = Query(None, description="Filter by status: pending, accepted, rejected"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar propuestas de intercambio para el usuario actual
    """
    logger.debug(f"Listing proposals for user {current_user.username}")
    
    # En MVP, usamos almacenamiento temporal
    user_proposals = proposal_store.get(current_user.id, [])
    
    # Filtrar por estado si se especifica
    if status_filter:
        user_proposals = [p for p in user_proposals if p.get('status', 'pending') == status_filter]
    else:
        # Por defecto, mostrar solo pendientes
        user_proposals = [p for p in user_proposals if p.get('status', 'pending') == 'pending']
    
    # Ordenar por fecha de creación (más recientes primero)
    user_proposals.sort(key=lambda x: x.get('created_at', 0), reverse=True)
    
    # Paginar
    paginated_proposals = user_proposals[skip:skip + limit]
    
    # Enriquecer con información de la base de datos si está disponible
    enriched_proposals = []
    for proposal in paginated_proposals:
        enriched = proposal.copy()
        
        # Añadir información de items si tenemos IDs
        if 'item_ids' in proposal:
            item_info = []
            for item_id in proposal['item_ids']:
                stmt = select(Item).where(Item.id == item_id)
                result = await db.execute(stmt)
                item = result.scalar_one_or_none()
                if item:
                    item_info.append({
                        'id': item.id,
                        'title': item.title,
                        'value': float(item.estimated_value)
                    })
            enriched['items_info'] = item_info
        
        enriched_proposals.append(enriched)
    
    return {
        "proposals": enriched_proposals,
        "total": len(user_proposals),
        "pending": len([p for p in user_proposals if p.get('status') == 'pending']),
        "accepted": len([p for p in user_proposals if p.get('status') == 'accepted']),
        "rejected": len([p for p in user_proposals if p.get('status') == 'rejected']),
        "skip": skip,
        "limit": limit
    }

@router.get("/{proposal_id}")
async def get_proposal(
    proposal_id: str,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener detalles de una propuesta específica
    """
    logger.debug(f"Getting proposal {proposal_id} for user {current_user.username}")
    
    # Buscar en almacenamiento temporal
    user_proposals = proposal_store.get(current_user.id, [])
    proposal = next((p for p in user_proposals if p.get('id') == proposal_id), None)
    
    if not proposal:
        logger.warning(f"Proposal {proposal_id} not found for user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    # Verificar que la propuesta pertenece al usuario
    if proposal.get('user_id') != current_user.id:
        logger.warning(f"Proposal {proposal_id} does not belong to user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this proposal"
        )
    
    # Enriquecer con información adicional
    enriched = proposal.copy()
    
    # Añadir información de items
    if 'item_ids' in proposal:
        items_info = []
        for item_id in proposal['item_ids']:
            stmt = select(Item).where(Item.id == item_id)
            result = await db.execute(stmt)
            item = result.scalar_one_or_none()
            if item:
                # Obtener dueño del item
                stmt_owner = select(User).where(User.id == item.user_id)
                result_owner = await db.execute(stmt_owner)
                owner = result_owner.scalar_one_or_none()
                
                items_info.append({
                    'id': item.id,
                    'title': item.title,
                    'description': item.description,
                    'value': float(item.estimated_value),
                    'condition': item.condition,
                    'category': item.category,
                    'owner': {
                        'username': owner.username if owner else 'Unknown',
                        'reputation': float(owner.reputation_score) if owner else 50.0
                    } if owner else None
                })
        enriched['items_detailed'] = items_info
    
    # Calcular tiempo restante si tiene expiración
    if 'expires_at' in proposal:
        current_time = time.time()
        expires_at = proposal['expires_at']
        if current_time < expires_at:
            enriched['time_remaining_hours'] = (expires_at - current_time) / 3600
            enriched['is_expired'] = False
        else:
            enriched['time_remaining_hours'] = 0
            enriched['is_expired'] = True
    
    return enriched

@router.post("/{proposal_id}/accept")
async def accept_proposal(
    proposal_id: str,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Aceptar una propuesta de intercambio
    """
    logger.info(f"User {current_user.username} accepting proposal {proposal_id}")
    
    # Buscar propuesta
    user_proposals = proposal_store.get(current_user.id, [])
    proposal_index = next((i for i, p in enumerate(user_proposals) if p.get('id') == proposal_id), None)
    
    if proposal_index is None:
        logger.warning(f"Proposal {proposal_id} not found for user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    proposal = user_proposals[proposal_index]
    
    # Verificar estado
    if proposal.get('status') != 'pending':
        logger.warning(f"Proposal {proposal_id} is not pending (status: {proposal.get('status')})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proposal is not pending (current status: {proposal.get('status')})"
        )
    
    # Verificar expiración
    if 'expires_at' in proposal and time.time() > proposal['expires_at']:
        logger.warning(f"Proposal {proposal_id} has expired")
        proposal['status'] = 'expired'
        proposal_store[current_user.id] = user_proposals
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Proposal has expired"
        )
    
    # Actualizar estado
    proposal['status'] = 'accepted'
    proposal['accepted_at'] = time.time()
    proposal['accepted_by'] = current_user.username
    
    # Marcar items como pendientes si tenemos IDs
    if 'item_ids' in proposal:
        for item_id in proposal['item_ids']:
            stmt = select(Item).where(
                Item.id == item_id,
                Item.user_id == current_user.id
            )
            result = await db.execute(stmt)
            item = result.scalar_one_or_none()
            
            if item and item.status == 'available':
                item.status = 'pending'
                db.add(item)
    
    await db.commit()
    
    # Actualizar almacenamiento
    proposal_store[current_user.id] = user_proposals
    
    logger.info(f"Proposal {proposal_id} accepted by user {current_user.username}")
    
    return {
        "success": True,
        "message": "Proposal accepted successfully",
        "proposal_id": proposal_id,
        "status": "accepted",
        "next_steps": [
            "Wait for other participants to accept",
            "Once all accept, arrange shipping",
            "Complete payment adjustments if needed"
        ]
    }

@router.post("/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: str,
    reason: Optional[str] = Query(None, description="Reason for rejection"),
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Rechazar una propuesta de intercambio
    """
    logger.info(f"User {current_user.username} rejecting proposal {proposal_id}")
    
    # Buscar propuesta
    user_proposals = proposal_store.get(current_user.id, [])
    proposal_index = next((i for i, p in enumerate(user_proposals) if p.get('id') == proposal_id), None)
    
    if proposal_index is None:
        logger.warning(f"Proposal {proposal_id} not found for user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    proposal = user_proposals[proposal_index]
    
    # Verificar estado
    if proposal.get('status') != 'pending':
        logger.warning(f"Proposal {proposal_id} is not pending (status: {proposal.get('status')})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proposal is not pending (current status: {proposal.get('status')})"
        )
    
    # Actualizar estado
    proposal['status'] = 'rejected'
    proposal['rejected_at'] = time.time()
    proposal['rejection_reason'] = reason or "No reason provided"
    
    # Actualizar almacenamiento
    proposal_store[current_user.id] = user_proposals
    
    logger.info(f"Proposal {proposal_id} rejected by user {current_user.username}")
    
    return {
        "success": True,
        "message": "Proposal rejected",
        "proposal_id": proposal_id,
        "status": "rejected",
        "reason": reason,
        "note": "You may receive new proposals in the future"
    }

@router.post("/{proposal_id}/counter")
async def counter_proposal(
    proposal_id: str,
    counter_data: dict,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Hacer una contrapropuesta (modificar términos)
    """
    logger.info(f"User {current_user.username} making counter-proposal for {proposal_id}")
    
    # Buscar propuesta original
    user_proposals = proposal_store.get(current_user.id, [])
    proposal_index = next((i for i, p in enumerate(user_proposals) if p.get('id') == proposal_id), None)
    
    if proposal_index is None:
        logger.warning(f"Proposal {proposal_id} not found for user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    original_proposal = user_proposals[proposal_index]
    
    # Verificar estado
    if original_proposal.get('status') != 'pending':
        logger.warning(f"Proposal {proposal_id} is not pending")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only counter pending proposals"
        )
    
    # Crear nueva propuesta basada en la original con modificaciones
    counter_proposal = original_proposal.copy()
    counter_proposal['id'] = f"{proposal_id}_counter_{int(time.time())}"
    counter_proposal['original_proposal_id'] = proposal_id
    counter_proposal['status'] = 'counter'
    counter_proposal['created_at'] = time.time()
    counter_proposal['is_counter'] = True
    counter_proposal['counter_details'] = counter_data
    
    # Aplicar modificaciones de la contrapropuesta
    if 'financial_adjustment' in counter_data:
        counter_proposal['financial_adjustment'] = counter_data['financial_adjustment']
    
    if 'note' in counter_data:
        counter_proposal['counter_note'] = counter_data['note']
    
    # Marcar original como "countered"
    original_proposal['status'] = 'countered'
    original_proposal['countered_at'] = time.time()
    
    # Añadir nueva propuesta
    user_proposals.append(counter_proposal)
    proposal_store[current_user.id] = user_proposals
    
    logger.info(f"Counter-proposal created for {proposal_id}")
    
    return {
        "success": True,
        "message": "Counter-proposal created",
        "original_proposal_id": proposal_id,
        "counter_proposal_id": counter_proposal['id'],
        "status": "counter_sent",
        "note": "The other participants will review your counter-proposal"
    }

@router.delete("/{proposal_id}")
async def delete_proposal(
    proposal_id: str,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar una propuesta (solo propuestas rechazadas o expiradas)
    """
    logger.info(f"User {current_user.username} deleting proposal {proposal_id}")
    
    # Buscar propuesta
    user_proposals = proposal_store.get(current_user.id, [])
    proposal_index = next((i for i, p in enumerate(user_proposals) if p.get('id') == proposal_id), None)
    
    if proposal_index is None:
        logger.warning(f"Proposal {proposal_id} not found for user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    proposal = user_proposals[proposal_index]
    
    # Verificar que se puede eliminar (solo rechazadas o expiradas)
    allowed_statuses = ['rejected', 'expired', 'cancelled']
    if proposal.get('status') not in allowed_statuses:
        logger.warning(f"Cannot delete proposal with status {proposal.get('status')}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can only delete proposals with status: {', '.join(allowed_statuses)}"
        )
    
    # Eliminar
    del user_proposals[proposal_index]
    proposal_store[current_user.id] = user_proposals
    
    logger.info(f"Proposal {proposal_id} deleted by user {current_user.username}")
    
    return {
        "success": True,
        "message": "Proposal deleted",
        "proposal_id": proposal_id,
        "deleted_at": time.time()
    }

@router.get("/stats/summary")
async def get_proposals_summary(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener resumen de propuestas
    """
    logger.debug(f"Getting proposals summary for user {current_user.username}")
    
    user_proposals = proposal_store.get(current_user.id, [])
    
    if not user_proposals:
        return {
            "total": 0,
            "by_status": {},
            "by_type": {},
            "acceptance_rate": 0,
            "avg_value": 0
        }
    
    # Calcular estadísticas
    by_status = {}
    by_type = {}
    total_value = 0
    accepted_count = 0
    total_considered = 0
    
    for proposal in user_proposals:
        # Por estado
        status = proposal.get('status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1
        
        # Por tipo
        type_ = proposal.get('exchange_type', 'unknown')
        by_type[type_] = by_type.get(type_, 0) + 1
        
        # Valor total
        if 'total_value' in proposal:
            total_value += proposal['total_value']
        
        # Tasa de aceptación
        if status in ['accepted', 'rejected', 'countered']:
            total_considered += 1
            if status == 'accepted':
                accepted_count += 1
    
    acceptance_rate = accepted_count / total_considered if total_considered > 0 else 0
    avg_value = total_value / len(user_proposals) if user_proposals else 0
    
    return {
        "total": len(user_proposals),
        "by_status": by_status,
        "by_type": by_type,
        "acceptance_rate": acceptance_rate,
        "avg_value": avg_value,
        "last_30_days": len([p for p in user_proposals if p.get('created_at', 0) > time.time() - (30 * 24 * 3600)]),
        "pending_now": by_status.get('pending', 0),
        "most_common_type": max(by_type.items(), key=lambda x: x[1])[0] if by_type else 'none'
    }

@router.post("/demo/generate")
async def generate_demo_proposals(
    count: int = Query(3, ge=1, le=10, description="Number of demo proposals to generate"),
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Generar propuestas de demostración (solo para desarrollo)
    """
    from ..utils.config import settings
    if settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBORBIDDEN,
            detail="Demo endpoints are not available in production"
        )
    
    logger.info(f"Generating {count} demo proposals for user {current_user.username}")
    
    # Obtener items del usuario para las demo
    stmt_items = select(Item).where(
        Item.user_id == current_user.id,
        Item.status == "available"
    ).limit(3)
    
    result_items = await db.execute(stmt_items)
    user_items = result_items.scalars().all()
    
    if not user_items:
        # Crear items de demo si el usuario no tiene
        demo_items = [
            {"title": "iPhone 13", "value": 600.0},
            {"title": "MacBook Air M1", "value": 800.0},
            {"title": "Bicicleta carretera", "value": 400.0}
        ]
    else:
        demo_items = [
            {"title": item.title, "value": float(item.estimated_value)}
            for item in user_items[:3]
        ]
    
    # Generar propuestas de demo
    demo_proposals = []
    
    for i in range(count):
        proposal_id = f"demo_{current_user.id}_{int(time.time())}_{i}"
        
        # Tipos de propuestas de demo
        if i % 3 == 0:
            # Intercambio directo
            proposal = {
                "id": proposal_id,
                "user_id": current_user.id,
                "title": f"Demo Direct Exchange: {demo_items[0]['title']} for MacBook Air M1",
                "summary": f"You give {demo_items[0]['title']} (€{demo_items[0]['value']}) for MacBook Air M1 (€800.0)",
                "financial_adjustment": f"Pay €212.00 total (€200.00 difference + €12.00 Treqe commission)",
                "benefits": [
                    "You get EXACTLY the MacBook you wanted",
                    "Direct exchange with one other user",
                    "Simple and fast"
                ],
                "recommended_action": "ACCEPT DEMO EXCHANGE",
                "net_result": f"You give €{demo_items[0]['value']} value, receive €800.0 value, pay €212 = NET: €{demo_items[0]['value']}",
                "exchange_type": "direct",
                "k_size": 2,
                "status": "pending",
                "created_at": time.time(),
                "expires_at": time.time() + (24 * 3600),  # 24 horas
                "is_demo": True,
                "item_ids": [item.id for item in user_items[:1]] if user_items else []
            }
        
        elif i % 3 == 1:
            # Ciclo k=3
            proposal = {
                "id": proposal_id,
                "user_id": current_user.id,
                "title": f"Demo Cycle Exchange: {demo_items[0]['title']} → MacBook → Bicicleta → {demo_items[0]['title']}",
                "summary": "3-user circular exchange",
                "financial_adjustment": f"Pay €212.00 (€200 difference + €12 commission)",
                "benefits": [
                    "Complex exchange that wouldn't be possible with direct trading",
                    "Everyone gets exactly what they want",
                    "Demonstrates Treqe's unique value"
                ],
                "recommended_action": "ACCEPT DEMO CYCLE",
                "net_result": "Economic tie, you gain convenience",
                "exchange_type": "cycle",
                "k_size": 3,
                "status": "pending",
                "created_at": time.time(),
                "expires_at": time.time() + (48 * 3600),  # 48 horas
                "is_demo": True,
                "item_ids": [item.id for item in user_items[:2]] if len(user_items) >= 2 else []
            }
        
        else:
            # Intercambio con ajuste positivo
            proposal = {
                "id": proposal_id,
                "user_id": current_user.id,
                "title": f"Demo Favorable Exchange: {demo_items[0]['title']} for {demo_items[1]['title'] if len(demo_items) > 1 else 'Item'} + Cash",
                "summary": f"You give {demo_items[0]['title']} (€{demo_items[0]['value']}) for {demo_items[1]['title'] if len(demo_items) > 1 else 'Item'} (€{demo_items[1]['value'] if len(demo_items) > 1 else 400.0})",
                "financial_adjustment": f"Receive €176.00 (€200 difference - €24 Treqe commission)",
                "benefits": [
                    "You get the item you want",
                    "You receive cash in addition",
                    "Great value proposition"
                ],
                "recommended_action": "ACCEPT AND RECEIVE CASH",
                "net_result": f"You give €{demo_items[0]['value']} value, receive €{demo_items[1]['value'] if len(demo_items) > 1 else 400.0} value + €176 = NET: €{demo_items[0]['value']}",
                "exchange_type": "direct",
                "k_size": 2,
                "status": "pending",
                "created_at": time.time(),
                "expires_at": time.time() + (12 * 3600),  # 12 horas
                "is_demo": True,
                "item_ids": [item.id for item in user_items[:1]] if user_items else []
            }
        
        demo_proposals.append(proposal)
    
    # Almacenar en el store del usuario
    if current_user.id not in proposal_store:
        proposal_store[current_user.id] = []
    
    proposal_store[current_user.id].extend(demo_proposals)
    
    return {
        "success": True,
        "generated": count,
        "proposal_ids": [p['id'] for p in demo_proposals],
        "note": "These are demo proposals for testing purposes only",
        "expire_in_hours": 24
    }