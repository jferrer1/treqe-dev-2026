"""
Endpoints API para gestión de items (ofertas)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional

from .schemas import ItemCreate, ItemUpdate, ItemResponse, ErrorResponse
from .auth import CurrentUser
from ..database.connection import get_db
from ..database.models import Item, User
from ..utils.logger import get_logger

logger = get_logger("api.items")

router = APIRouter()

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Crear nuevo item (oferta)
    """
    logger.info(f"Creating item for user {current_user.username}: {item_data.title}")
    
    # Verificar límite de items activos (opcional)
    stmt_count = select(Item).where(
        Item.user_id == current_user.id,
        Item.status == "available"
    )
    result_count = await db.execute(stmt_count)
    active_items = len(result_count.scalars().all())
    
    # Límite de 10 items activos por usuario
    if active_items >= 10:
        logger.warning(f"User {current_user.username} has reached item limit ({active_items})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 10 active items reached. Please deactivate or exchange some items first."
        )
    
    # Crear item
    db_item = Item(
        user_id=current_user.id,
        title=item_data.title,
        description=item_data.description,
        category=item_data.category,
        estimated_value=item_data.estimated_value,
        condition=item_data.condition,
        photos=item_data.photos or [],
        status="available"
    )
    
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    
    # Cargar relación owner para la respuesta
    await db.refresh(db_item, ["owner"])
    
    logger.info(f"Item created successfully: {db_item.title} (ID: {db_item.id})")
    
    return db_item

@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0, description="Número de items a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de items a retornar"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_value: Optional[float] = Query(None, ge=0, description="Valor mínimo"),
    max_value: Optional[float] = Query(None, ge=0, description="Valor máximo"),
    condition: Optional[str] = Query(None, description="Filtrar por condición"),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar items disponibles con filtros
    """
    logger.debug(f"Listing items: skip={skip}, limit={limit}, category={category}")
    
    # Construir query base
    stmt = select(Item).where(
        Item.status == "available"
    ).join(User).where(
        User.is_active == True
    )
    
    # Aplicar filtros
    if category:
        stmt = stmt.where(Item.category.ilike(f"%{category}%"))
    
    if min_value is not None:
        stmt = stmt.where(Item.estimated_value >= min_value)
    
    if max_value is not None:
        stmt = stmt.where(Item.estimated_value <= max_value)
    
    if condition:
        stmt = stmt.where(Item.condition == condition)
    
    # Ordenar y paginar
    stmt = stmt.order_by(Item.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    logger.debug(f"Found {len(items)} items")
    
    return items

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener item por ID
    """
    logger.debug(f"Getting item ID: {item_id}")
    
    stmt = select(Item).where(
        Item.id == item_id,
        Item.status == "available"
    ).join(User).where(
        User.is_active == True
    )
    
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not found or not available: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not available"
        )
    
    return item

@router.get("/by-uuid/{item_uuid}", response_model=ItemResponse)
async def get_item_by_uuid(
    item_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener item por UUID
    """
    logger.debug(f"Getting item UUID: {item_uuid}")
    
    stmt = select(Item).where(
        Item.uuid == item_uuid,
        Item.status == "available"
    ).join(User).where(
        User.is_active == True
    )
    
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not found or not available: {item_uuid}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not available"
        )
    
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar item propio
    """
    logger.info(f"Updating item {item_id} for user {current_user.username}")
    
    # Obtener item
    stmt = select(Item).where(
        Item.id == item_id,
        Item.user_id == current_user.id
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not found or not owned by user: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission to update it"
        )
    
    # Verificar que no esté en un intercambio pendiente
    if item.status == "pending":
        logger.warning(f"Cannot update item in pending exchange: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update item that is part of a pending exchange"
        )
    
    # Actualizar campos
    update_data = item_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(item, field) and value is not None:
            setattr(item, field, value)
    
    db.add(item)
    await db.commit()
    await db.refresh(item)
    await db.refresh(item, ["owner"])
    
    logger.info(f"Item updated successfully: {item.title} (ID: {item.id})")
    
    return item

@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar item propio
    """
    logger.info(f"Deleting item {item_id} for user {current_user.username}")
    
    # Obtener item
    stmt = select(Item).where(
        Item.id == item_id,
        Item.user_id == current_user.id
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not found or not owned by user: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission to delete it"
        )
    
    # Verificar que no esté en un intercambio
    if item.status == "pending":
        logger.warning(f"Cannot delete item in pending exchange: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete item that is part of a pending exchange"
        )
    
    # En lugar de eliminar, marcar como eliminado (soft delete)
    item.status = "deleted"
    db.add(item)
    await db.commit()
    
    logger.info(f"Item marked as deleted: {item.title} (ID: {item.id})")
    
    return {
        "message": "Item deleted successfully",
        "item_id": item_id,
        "title": item.title
    }

@router.get("/me/items", response_model=List[ItemResponse])
async def get_my_items(
    current_user: User = CurrentUser,
    status_filter: Optional[str] = Query(None, description="Filtrar por estado: available, pending, exchanged"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener items del usuario actual
    """
    logger.debug(f"Getting items for user {current_user.username}")
    
    stmt = select(Item).where(Item.user_id == current_user.id)
    
    if status_filter:
        stmt = stmt.where(Item.status == status_filter)
    else:
        # Excluir items eliminados por defecto
        stmt = stmt.where(Item.status != "deleted")
    
    stmt = stmt.order_by(Item.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    logger.debug(f"Found {len(items)} items for user {current_user.username}")
    
    return items

@router.post("/{item_id}/mark-pending")
async def mark_item_pending(
    item_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Marcar item como pendiente (cuando entra en un intercambio)
    """
    logger.info(f"Marking item {item_id} as pending for user {current_user.username}")
    
    stmt = select(Item).where(
        Item.id == item_id,
        Item.user_id == current_user.id,
        Item.status == "available"
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not available or not owned by user: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, not available, or not owned by you"
        )
    
    item.status = "pending"
    db.add(item)
    await db.commit()
    
    logger.info(f"Item marked as pending: {item.title} (ID: {item.id})")
    
    return {
        "message": "Item marked as pending",
        "item_id": item_id,
        "status": "pending"
    }

@router.post("/{item_id}/mark-available")
async def mark_item_available(
    item_id: int,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Marcar item como disponible nuevamente
    """
    logger.info(f"Marking item {item_id} as available for user {current_user.username}")
    
    stmt = select(Item).where(
        Item.id == item_id,
        Item.user_id == current_user.id,
        Item.status == "pending"
    )
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        logger.warning(f"Item not pending or not owned by user: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, not pending, or not owned by you"
        )
    
    item.status = "available"
    db.add(item)
    await db.commit()
    
    logger.info(f"Item marked as available: {item.title} (ID: {item.id})")
    
    return {
        "message": "Item marked as available",
        "item_id": item_id,
        "status": "available"
    }

@router.get("/search/suggestions")
async def get_search_suggestions(
    query: str = Query(..., min_length=2, description="Texto para búsqueda"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener sugerencias de búsqueda para items
    """
    logger.debug(f"Getting search suggestions for: {query}")
    
    # Búsqueda en título y categoría
    stmt = select(Item).where(
        Item.status == "available",
        or_(
            Item.title.ilike(f"%{query}%"),
            Item.category.ilike(f"%{query}%"),
            Item.description.ilike(f"%{query}%")
        )
    ).join(User).where(
        User.is_active == True
    ).limit(limit)
    
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    # Extraer sugerencias únicas de categorías
    categories = set()
    titles = []
    
    for item in items:
        categories.add(item.category)
        titles.append(item.title)
    
    suggestions = {
        "categories": list(categories)[:5],
        "titles": titles[:10],
        "total_items": len(items),
        "query": query
    }
    
    return suggestions

@router.get("/categories/popular")
async def get_popular_categories(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener categorías más populares
    """
    logger.debug(f"Getting popular categories, limit: {limit}")
    
    # En una implementación real, esto usaría una consulta GROUP BY
    # Por ahora, devolveremos categorías predefinidas
    popular_categories = [
        {"name": "Electrónica", "count": 125, "icon": "📱"},
        {"name": "Hogar", "count": 89, "icon": "🏠"},
        {"name": "Ropa", "count": 76, "icon": "👕"},
        {"name": "Deportes", "count": 54, "icon": "⚽"},
        {"name": "Libros", "count": 42, "icon": "📚"},
        {"name": "Juguetes", "count": 38, "icon": "🎮"},
        {"name": "Muebles", "count": 35, "icon": "🛋️"},
        {"name": "Herramientas", "count": 29, "icon": "🛠️"},
        {"name": "Cocina", "count": 27, "icon": "🍳"},
        {"name": "Jardín", "count": 21, "icon": "🌿"}
    ]
    
    return {
        "categories": popular_categories[:limit],
        "total_categories": len(popular_categories)
    }