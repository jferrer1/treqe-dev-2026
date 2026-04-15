"""
Autenticación JWT para Treqe API
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import TokenData
from ..database.connection import get_db
from ..database.models import User
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("auth")

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear token JWT de acceso"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Crear token JWT de refresh"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    """Autenticar usuario con username/email y contraseña"""
    # Buscar por username o email
    stmt = select(User).where(
        (User.username == username) | (User.email == username)
    ).where(User.is_active == True)
    
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Obtener usuario actual a partir del token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_id: int = payload.get("user_id")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id, username=payload.get("username", ""))
    
    except JWTError:
        raise credentials_exception
    
    # Buscar usuario en base de datos
    stmt = select(User).where(User.id == token_data.user_id, User.is_active == True)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual está activo"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario actual es administrador"""
    # Por ahora, todos los usuarios pueden hacer todo
    # En el futuro, añadir campo is_admin al modelo User
    return current_user

def decode_token(token: str) -> Optional[dict]:
    """Decodificar token JWT sin verificar usuario"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

async def refresh_access_token(refresh_token: str, db: AsyncSession) -> Optional[str]:
    """Obtener nuevo access token a partir de refresh token"""
    payload = decode_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        return None
    
    user_id = payload.get("user_id")
    if not user_id:
        return None
    
    # Verificar que el usuario existe y está activo
    stmt = select(User).where(User.id == user_id, User.is_active == True)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    # Crear nuevo access token
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username}
    )
    
    return access_token

# Dependencias para inyección
CurrentUser = Depends(get_current_active_user)
OptionalCurrentUser = Depends(get_current_user)  # Usuario opcional para algunos endpoints

__all__ = [
    "pwd_context",
    "security",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "authenticate_user",
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "decode_token",
    "refresh_access_token",
    "CurrentUser",
    "OptionalCurrentUser",
]