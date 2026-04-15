"""
Endpoints API para gestión de preferencias (demandas)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional

from .schemas import PreferenceCreate, PreferenceUpdate, PreferenceResponse, ErrorResponse
from .auth import CurrentUser
from ..database.connection import get_db
from ..database.models import Preference, Item, User
from ..utils.logger import get_logger

logger = get_logger("api.preferences")

router = APIRouter()

@router.post("/", response_model=PreferenceResponse, status_code=status.HTTP_201_CREATED)
async def create_preference(
    preference_data: PreferenceCreate,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Crear nueva preferencia (qué item quiere el usuario)
    """
    logger.info(f"Creating preference for user {current_user.username}")
    
    # Verificar que el item existe y pertenece al usuario
    stmt_item = select(Item).where(
        Item.id == preference_data.item_id,
        Item.user_id == current_user.id,
        Item.status == "available"
    )
    result_item = await db.execute(stmt_item)
    item = result_item.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not found or not available: {preference_data.item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, not available, or not owned by you"
        )
    
    # Verificar límite de preferencias activas (máximo 5)
    stmt_count = select(Preference).where(
        Preference.user_id == current_user.id,
        Preference.is_active == True
    )
    result_count = await db.execute(stmt_count)
    active_preferences = len(result_count.scalars().all())
    
    if active_preferences >= 5:
        logger.warning(f"User {current_user.username} has reached preference limit ({active_preferences})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 5 active preferences reached. Please deactivate some preferences first."
        )
    
    # Verificar que no existe ya una preferencia similar
    stmt_existing = select(Preference).where(
        Preference.user_id == current_user.id,
        Preference.item_id == preference_data.item_id,
        Preference.desired_item_title.ilike(preference_data.desired_item_title),
        Preference.is_active == True
    )
    result_existing = await db.execute(stmt_existing)
    existing_preference = result_existing.scalar_one_or_none()
    
    if existing_preference:
        logger.warning(f"Similar preference already exists for user {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A similar preference already exists for this item"
        )
    
    # Crear preferencia
    db_preference = Preference(
        user_id=current_user.id,
        item_id=preference_data.item_id,
        desired_item_title=preference_data.desired_item_title,
        desired_category=preference_data.desired_category,
        min_value=preference_data.min_value,
        max_value=preference_data.max_value,
        priority=preference_data.priority,
        is_active=True
    )
    
    db.add(db_preference)
    await db.commit()
    await db.refresh(db_preference)
    
    # Cargar relaciones para la respuesta
    await db.refresh(db_preference, ["user", "item"])
    if db_preference.item:
        await db.refresh(db_preference.item, ["owner"])
    
    logger.info(f"Preference created successfully for user {current_user.username}")
    
    return db_preference

@router.get("/", response_model=List[PreferenceResponse])
async def list_preferences(
    current_user: User = CurrentUser,
    active_only: bool = Query(True, description="Mostrar solo preferencias activas"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar preferencias del usuario actual
    """
    logger.debug(f"Listing preferences for user {current_user.username}")
    
    stmt = select(Preference).where(Preference.user_id == current_user.id)
    
    if active_only:
        stmt = stmt.where(Preference.is_active == True)
    
    stmt = stmt.order_by(
        Preference.priority.desc(),
        Preference.created_at.desc()
    ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    preferences = result.scalars().all()
    
    # Cargar relaciones
    for pref in preferences:
        await db.refresh(pref, ["user", "item"])
        if pref.item:
            await db.refresh(pref.item, ["owner"])
    
    logger.debug(f"Found {len(preferences)} preferences for user {current_user.username}")
    
    return preferences

@router.get("/{preference_id}", response_model=PreferenceResponse)
async def get_preference(
    preference_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener preferencia específica
    """
    logger.debug(f"Getting preference {preference_id} for user {current_user.username}")
    
    stmt = select(Preference).where(
        Preference.id == preference_id,
        Preference.user_id == current_user.id
    )
    
    result = await db.execute(stmt)
    preference = result.scalar_one_or_none()
    
    if not preference:
        logger.warning(f"Preference not found: {preference_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )
    
    # Cargar relaciones
    await db.refresh(preference, ["user", "item"])
    if preference.item:
        await db.refresh(preference.item, ["owner"])
    
    return preference

@router.put("/{preference_id}", response_model=PreferenceResponse)
async def update_preference(
    preference_id: int,
    preference_data: PreferenceUpdate,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar preferencia
    """
    logger.info(f"Updating preference {preference_id} for user {current_user.username}")
    
    # Obtener preferencia
    stmt = select(Preference).where(
        Preference.id == preference_id,
        Preference.user_id == current_user.id
    )
    result = await db.execute(stmt)
    preference = result.scalar_one_or_none()
    
    if not preference:
        logger.warning(f"Preference not found: {preference_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )
    
    # Actualizar campos
    update_data = preference_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(preference, field) and value is not None:
            setattr(preference, field, value)
    
    db.add(preference)
    await db.commit()
    await db.refresh(preference)
    
    # Cargar relaciones
    await db.refresh(preference, ["user", "item"])
    if preference.item:
        await db.refresh(preference.item, ["owner"])
    
    logger.info(f"Preference updated successfully: {preference_id}")
    
    return preference

@router.delete("/{preference_id}")
async def delete_preference(
    preference_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar preferencia (soft delete - marcar como inactiva)
    """
    logger.info(f"Deleting preference {preference_id} for user {current_user.username}")
    
    # Obtener preferencia
    stmt = select(Preference).where(
        Preference.id == preference_id,
        Preference.user_id == current_user.id
    )
    result = await db.execute(stmt)
    preference = result.scalar_one_or_none()
    
    if not preference:
        logger.warning(f"Preference not found: {preference_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )
    
    # Marcar como inactiva en lugar de eliminar
    preference.is_active = False
    db.add(preference)
    await db.commit()
    
    logger.info(f"Preference marked as inactive: {preference_id}")
    
    return {
        "message": "Preference deleted successfully",
        "preference_id": preference_id,
        "desired_item": preference.desired_item_title
    }

@router.post("/{preference_id}/activate")
async def activate_preference(
    preference_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Activar preferencia previamente inactiva
    """
    logger.info(f"Activating preference {preference_id} for user {current_user.username}")
    
    # Obtener preferencia
    stmt = select(Preference).where(
        Preference.id == preference_id,
        Preference.user_id == current_user.id,
        Preference.is_active == False
    )
    result = await db.execute(stmt)
    preference = result.scalar_one_or_none()
    
    if not preference:
        logger.warning(f"Inactive preference not found: {preference_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inactive preference not found"
        )
    
    # Verificar límite de preferencias activas
    stmt_count = select(Preference).where(
        Preference.user_id == current_user.id,
        Preference.is_active == True
    )
    result_count = await db.execute(stmt_count)
    active_preferences = len(result_count.scalars().all())
    
    if active_preferences >= 5:
        logger.warning(f"User {current_user.username} has reached preference limit ({active_preferences})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 5 active preferences reached. Please deactivate another preference first."
        )
    
    # Activar preferencia
    preference.is_active = True
    db.add(preference)
    await db.commit()
    
    logger.info(f"Preference activated: {preference_id}")
    
    return {
        "message": "Preference activated successfully",
        "preference_id": preference_id,
        "is_active": True
    }

@router.post("/{preference_id}/deactivate")
async def deactivate_preference(
    preference_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Desactivar preferencia (mantener en historial pero no usarla para matching)
    """
    logger.info(f"Deactivating preference {preference_id} for user {current_user.username}")
    
    # Obtener preferencia
    stmt = select(Preference).where(
        Preference.id == preference_id,
        Preference.user_id == current_user.id,
        Preference.is_active == True
    )
    result = await db.execute(stmt)
    preference = result.scalar_one_or_none()
    
    if not preference:
        logger.warning(f"Active preference not found: {preference_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active preference not found"
        )
    
    # Desactivar preferencia
    preference.is_active = False
    db.add(preference)
    await db.commit()
    
    logger.info(f"Preference deactivated: {preference_id}")
    
    return {
        "message": "Preference deactivated successfully",
        "preference_id": preference_id,
        "is_active": False
    }

@router.get("/me/stats")
async def get_preferences_stats(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener estadísticas de preferencias del usuario
    """
    logger.debug(f"Getting preference stats for user {current_user.username}")
    
    # Todas las preferencias del usuario
    stmt = select(Preference).where(Preference.user_id == current_user.id)
    result = await db.execute(stmt)
    all_preferences = result.scalars().all()
    
    # Calcular estadísticas
    total = len(all_preferences)
    active = len([p for p in all_preferences if p.is_active])
    inactive = total - active
    
    # Distribución por prioridad
    priority_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for pref in all_preferences:
        if pref.priority in priority_counts:
            priority_counts[pref.priority] += 1
    
    # Categorías más deseadas
    categories = {}
    for pref in all_preferences:
        if pref.desired_category:
            categories[pref.desired_category] = categories.get(pref.desired_category, 0) + 1
    
    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
    
    stats = {
        "total": total,
        "active": active,
        "inactive": inactive,
        "priority_distribution": priority_counts,
        "top_categories": [{"category": cat, "count": count} for cat, count in top_categories],
        "average_priority": sum(p.priority for p in all_preferences) / total if total > 0 else 0
    }
    
    return stats

@router.get("/search/compatible-items")
async def search_compatible_items(
    preference_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Buscar items compatibles con una preferencia específica
    """
    logger.debug(f"Searching compatible items for preference {preference_id}")
    
    # Obtener preferencia
    stmt_pref = select(Preference).where(Preference.id == preference_id)
    result_pref = await db.execute(stmt_pref)
    preference = result_pref.scalar_one_or_none()
    
    if not preference:
        logger.warning(f"Preference not found: {preference_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )
    
    # Construir query para items compatibles
    stmt_items = select(Item).where(
        Item.status == "available",
        Item.user_id != preference.user_id,  # No mostrar items del mismo usuario
        Item.title.ilike(f"%{preference.desired_item_title}%")
    ).join(User).where(
        User.is_active == True
    )
    
    # Filtrar por categoría si está especificada
    if preference.desired_category:
        stmt_items = stmt_items.where(Item.category.ilike(f"%{preference.desired_category}%"))
    
    # Filtrar por valor si está especificado
    if preference.min_value is not None:
        stmt_items = stmt_items.where(Item.estimated_value >= preference.min_value)
    
    if preference.max_value is not None:
        stmt_items = stmt_items.where(Item.estimated_value <= preference.max_value)
    
    # Ordenar por compatibilidad (simplificado)
    stmt_items = stmt_items.order_by(
        Item.estimated_value.desc()  # Items de mayor valor primero
    ).offset(skip).limit(limit)
    
    result_items = await db.execute(stmt_items)
    compatible_items = result_items.scalars().all()
    
    # Calcular score de compatibilidad para cada item
    items_with_score = []
    for item in compatible_items:
        score = calculate_compatibility_score(preference, item)
        items_with_score.append({
            "item": item,
            "compatibility_score": score,
            "value_match": abs(float(item.estimated_value) - float(preference.item.estimated_value)) if preference.item else 0
        })
    
    # Ordenar por score de compatibilidad
    items_with_score.sort(key=lambda x: x["compatibility_score"], reverse=True)
    
    return {
        "preference": {
            "id": preference.id,
            "desired_item_title": preference.desired_item_title,
            "desired_category": preference.desired_category
        },
        "compatible_items": [
            {
                "item": item_data["item"],
                "compatibility_score": item_data["compatibility_score"],
                "value_difference": item_data["value_match"]
            }
            for item_data in items_with_score
        ],
        "total_found": len(compatible_items),
        "skip": skip,
        "limit": limit
    }

def calculate_compatibility_score(preference: Preference, item: Item) -> float:
    """
    Calcular score de compatibilidad entre preferencia e item
    """
    score = 0.0
    
    # Coincidencia de título (0-50 puntos)
    if preference.desired_item_title.lower() in item.title.lower():
        score += 30
    elif any(word in item.title.lower() for word in preference.desired_item_title.lower().split()):
        score += 20
    
    # Coincidencia de categoría (0-30 puntos)
    if preference.desired_category and item.category:
        if preference.desired_category.lower() == item.category.lower():
            score += 30
        elif preference.desired_category.lower() in item.category.lower():
            score += 20
    
    # Coincidencia de valor (0-20 puntos)
    if preference.min_value and preference.max_value:
        item_value = float(item.estimated_value)
        if preference.min_value <= item_value <= preference.max_value:
            score += 20
        elif abs(item_value - (preference.min_value + preference.max_value) / 2) <= (preference.max_value - preference.min_value):
            score += 10
    
    return min(score, 100.0)  # Máximo 100 puntos