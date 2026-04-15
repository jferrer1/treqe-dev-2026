"""
Router simplificado de usuarios para pruebas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from ..database.connection import get_db
from ..database.models import User
from .schemas_simple import UserCreate, UserLogin, UserResponse, Token, Message
from ..utils.auth import create_access_token, create_refresh_token, verify_password

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registrar nuevo usuario"""
    try:
        # Verificar si usuario ya existe
        stmt = select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        
        # Hash password
        password_hash = bcrypt.hashpw(
            user_data.password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Crear usuario
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            full_name=user_data.full_name,
            reputation_score=0.0,
            is_active=True
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login de usuario"""
    try:
        # Buscar usuario
        stmt = select(User).where(User.username == login_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verificar password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verificar usuario activo
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )
        
        # Crear tokens
        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(lambda: None)  # Placeholder para auth
):
    """Obtener usuario actual (simplificado para pruebas)"""
    # En una implementación real, esto usaría dependencia de autenticación
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented in simplified version"
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Obtener usuario por ID"""
    try:
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting user: {str(e)}"
        )