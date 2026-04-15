"""
Schemas simplificados para pruebas - Compatible con Pydantic V2
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Schemas base
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    reputation_score: float = 0.0

class UserCreate(BaseSchema):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseSchema):
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña")

class UserResponse(BaseSchema):
    id: int
    uuid: str
    username: str
    email: EmailStr
    full_name: Optional[str]
    reputation_score: float
    is_active: bool
    created_at: datetime

# Item schemas
class ItemBase(BaseSchema):
    title: str
    description: str
    category: str
    estimated_value: float
    condition: str = "good"

class ItemCreate(BaseSchema):
    title: str
    description: str
    category: str
    estimated_value: float
    condition: str = "good"

class ItemResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    description: str
    category: str
    estimated_value: float
    condition: str
    status: str
    created_at: datetime

# Preference schemas
class PreferenceBase(BaseSchema):
    desired_item_title: str
    desired_category: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    priority: int = 1

class PreferenceCreate(BaseSchema):
    item_id: int  # Item que el usuario está dispuesto a intercambiar
    desired_item_title: str
    desired_category: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    priority: int = 1

class PreferenceResponse(BaseSchema):
    id: int
    user_id: int
    item_id: int
    desired_item_title: str
    desired_category: Optional[str]
    min_value: Optional[float]
    max_value: Optional[float]
    priority: int
    is_active: bool
    created_at: datetime

# Matching schemas
class ExchangeCycle(BaseSchema):
    """Ciclo de intercambio encontrado"""
    k_size: int
    users: List[int]
    items: List[int]
    total_value: float
    commission_total: float
    net_adjustments: List[float]  # Ajustes monetarios por usuario

class MatchingRequest(BaseSchema):
    """Request para buscar intercambios"""
    user_id: int
    max_k: Optional[int] = 4
    timeout_seconds: Optional[int] = 5

class MatchingResponse(BaseSchema):
    """Response con intercambios encontrados"""
    user_id: int
    cycles_found: List[ExchangeCycle]
    search_time_ms: float
    total_cycles: int

# Token schemas
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseSchema):
    username: Optional[str] = None

# Message schemas
class Message(BaseSchema):
    message: str