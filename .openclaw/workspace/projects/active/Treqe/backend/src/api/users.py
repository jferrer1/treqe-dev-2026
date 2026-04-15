"""
Endpoints API para gestión de usuarios
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import (
    UserCreate, UserUpdate, UserLogin, UserResponse, 
    UserDetailResponse, Token, ErrorResponse
)
from .auth import (
    authenticate_user, create_access_token, create_refresh_token,
    get_password_hash, CurrentUser
)
from ..database.connection import get_db
from ..database.models import User, Item, Preference
from ..utils.logger import get_logger

logger = get_logger("api.users")

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registrar nuevo usuario
    """
    logger.info(f"Registering new user: {user_data.username}")
    
    # Verificar que el username no existe
    stmt = select(User).where(User.username == user_data.username)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        logger.warning(f"Username already exists: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verificar que el email no existe
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    existing_email = result.scalar_one_or_none()
    
    if existing_email:
        logger.warning(f"Email already exists: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Crear usuario
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        location=user_data.location,
        reputation_score=50.00,  # Valor inicial
        is_active=True,
        is_verified=False,  # Requerirá verificación por email
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    logger.info(f"User registered successfully: {db_user.username} (ID: {db_user.id})")
    
    return db_user

@router.post("/login", response_model=Token)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login de usuario (obtener tokens JWT)
    """
    logger.info(f"Login attempt for: {login_data.username or login_data.email}")
    
    # Autenticar usuario
    identifier = login_data.username or login_data.email
    user = await authenticate_user(db, identifier, login_data.password)
    
    if not user:
        logger.warning(f"Login failed for: {identifier}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        logger.warning(f"Inactive user attempted login: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Crear tokens
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username}
    )
    
    refresh_token = create_refresh_token(
        data={"user_id": user.id, "username": user.username}
    )
    
    logger.info(f"Login successful for user: {user.username} (ID: {user.id})")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutos
    }

@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_info(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener información del usuario actual
    """
    logger.debug(f"Getting info for user: {current_user.username}")
    
    # Contar items activos
    stmt_items = select(Item).where(Item.user_id == current_user.id, Item.status == "available")
    result_items = await db.execute(stmt_items)
    items_count = len(result_items.scalars().all())
    
    # Contar preferencias activas
    stmt_prefs = select(Preference).where(
        Preference.user_id == current_user.id, 
        Preference.is_active == True
    )
    result_prefs = await db.execute(stmt_prefs)
    preferences_count = len(result_prefs.scalars().all())
    
    # Contar intercambios (pendiente implementación)
    exchanges_count = 0
    
    user_response = UserDetailResponse(
        uuid=current_user.uuid,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        location=current_user.location,
        reputation_score=float(current_user.reputation_score),
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        items_count=items_count,
        preferences_count=preferences_count,
        exchanges_count=exchanges_count
    )
    
    return user_response

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar información del usuario actual
    """
    logger.info(f"Updating user: {current_user.username}")
    
    # Actualizar campos permitidos
    update_data = user_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(current_user, field) and value is not None:
            setattr(current_user, field, value)
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    
    logger.info(f"User updated successfully: {current_user.username}")
    
    return current_user

@router.get("/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener información pública de un usuario por username
    """
    logger.debug(f"Getting public info for user: {username}")
    
    stmt = select(User).where(
        User.username == username, 
        User.is_active == True
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        logger.warning(f"User not found: {username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/me/deactivate")
async def deactivate_current_user(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Desactivar cuenta del usuario actual
    """
    logger.info(f"Deactivating user: {current_user.username}")
    
    current_user.is_active = False
    db.add(current_user)
    await db.commit()
    
    logger.info(f"User deactivated: {current_user.username}")
    
    return {
        "message": "Account deactivated successfully",
        "user_id": current_user.id,
        "username": current_user.username
    }

@router.get("/me/items/count")
async def get_user_items_count(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener conteo de items del usuario
    """
    stmt = select(Item).where(Item.user_id == current_user.id)
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    counts = {
        "total": len(items),
        "available": len([i for i in items if i.status == "available"]),
        "pending": len([i for i in items if i.status == "pending"]),
        "exchanged": len([i for i in items if i.status == "exchanged"])
    }
    
    return counts

@router.get("/me/stats")
async def get_user_stats(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener estadísticas del usuario
    """
    # Items
    stmt_items = select(Item).where(Item.user_id == current_user.id)
    result_items = await db.execute(stmt_items)
    items = result_items.scalars().all()
    
    # Preferencias
    stmt_prefs = select(Preference).where(Preference.user_id == current_user.id)
    result_prefs = await db.execute(stmt_prefs)
    preferences = result_prefs.scalars().all()
    
    stats = {
        "items": {
            "total": len(items),
            "available": len([i for i in items if i.status == "available"]),
            "total_value": sum(float(i.estimated_value) for i in items if i.status == "available")
        },
        "preferences": {
            "total": len(preferences),
            "active": len([p for p in preferences if p.is_active])
        },
        "reputation": {
            "score": float(current_user.reputation_score),
            "level": get_reputation_level(float(current_user.reputation_score))
        },
        "account": {
            "created_at": current_user.created_at,
            "is_verified": current_user.is_verified,
            "days_active": (datetime.utcnow() - current_user.created_at).days if current_user.created_at else 0
        }
    }
    
    return stats

def get_reputation_level(score: float) -> str:
    """Determinar nivel de reputación basado en score"""
    if score >= 80:
        return "excellent"
    elif score >= 60:
        return "good"
    elif score >= 40:
        return "fair"
    else:
        return "poor"

# Error handlers
@router.get("/{username}/items")
async def get_user_items(
    username: str,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener items públicos de un usuario
    """
    # Primero obtener el usuario
    stmt_user = select(User).where(User.username == username, User.is_active == True)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener items disponibles
    stmt_items = select(Item).where(
        Item.user_id == user.id,
        Item.status == "available"
    ).offset(skip).limit(limit)
    
    result_items = await db.execute(stmt_items)
    items = result_items.scalars().all()
    
    return {
        "user": {
            "username": user.username,
            "location": user.location,
            "reputation_score": float(user.reputation_score)
        },
        "items": items,
        "count": len(items),
        "skip": skip,
        "limit": limit
    }