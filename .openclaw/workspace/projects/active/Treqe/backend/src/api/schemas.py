"""
Schemas Pydantic para validación de datos API
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ============================================================================
# SCHEMAS COMUNES
# ============================================================================

class BaseSchema(BaseModel):
    """Schema base con configuración común"""
    class Config:
        from_attributes = True
        populate_by_name = True

class TimestampMixin(BaseSchema):
    """Mixins para timestamps"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UUIDMixin(BaseSchema):
    """Mixins para UUID"""
    uuid: Optional[UUID] = None

# ============================================================================
# SCHEMAS DE USUARIO
# ============================================================================

class UserBase(BaseSchema):
    """Base para schemas de usuario"""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email del usuario")
    full_name: Optional[str] = Field(None, max_length=100, description="Nombre completo")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono")
    location: Optional[str] = Field(None, max_length=100, description="Ubicación")

class UserCreate(UserBase):
    """Schema para creación de usuario"""
    password: str = Field(..., min_length=8, max_length=100, description="Contraseña")
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Puedes añadir más validaciones de complejidad aquí
        return v

class UserUpdate(BaseSchema):
    """Schema para actualización de usuario"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class UserLogin(BaseSchema):
    """Schema para login de usuario"""
    username: Optional[str] = Field(None, description="Nombre de usuario o email")
    email: Optional[EmailStr] = Field(None, description="Email o nombre de usuario")
    password: str = Field(..., description="Contraseña")
    
    @validator('username', 'email')
    def validate_credentials(cls, v, values, field):
        if field.name == 'username' and not v and not values.get('email'):
            raise ValueError('Either username or email must be provided')
        if field.name == 'email' and not v and not values.get('username'):
            raise ValueError('Either username or email must be provided')
        return v

class UserResponse(UUIDMixin, TimestampMixin):
    """Schema para respuesta de usuario (público)"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    reputation_score: float = Field(default=50.0, ge=0.0, le=100.0)
    is_active: bool = True
    is_verified: bool = False

class UserDetailResponse(UserResponse):
    """Schema para respuesta detallada de usuario (privado)"""
    items_count: Optional[int] = 0
    preferences_count: Optional[int] = 0
    exchanges_count: Optional[int] = 0

# ============================================================================
# SCHEMAS DE ITEMS
# ============================================================================

class ItemBase(BaseSchema):
    """Base para schemas de item"""
    title: str = Field(..., min_length=3, max_length=200, description="Título del item")
    description: Optional[str] = Field(None, description="Descripción detallada")
    category: str = Field(..., max_length=50, description="Categoría del item")
    estimated_value: float = Field(..., gt=0, description="Valor estimado en EUR")
    condition: str = Field(..., description="Condición: new, like_new, good, fair")
    photos: Optional[List[str]] = Field(None, description="URLs de fotos")
    
    @validator('condition')
    def validate_condition(cls, v):
        valid_conditions = ['new', 'like_new', 'good', 'fair']
        if v not in valid_conditions:
            raise ValueError(f'Condition must be one of: {", ".join(valid_conditions)}')
        return v

class ItemCreate(ItemBase):
    """Schema para creación de item"""
    pass

class ItemUpdate(BaseSchema):
    """Schema para actualización de item"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    estimated_value: Optional[float] = None
    condition: Optional[str] = None
    photos: Optional[List[str]] = None
    status: Optional[str] = None

class ItemResponse(UUIDMixin, TimestampMixin):
    """Schema para respuesta de item"""
    title: str
    description: Optional[str] = None
    category: str
    estimated_value: float
    condition: str
    photos: Optional[List[str]] = None
    status: str = "available"
    owner: UserResponse

# ============================================================================
# SCHEMAS DE PREFERENCIAS
# ============================================================================

class PreferenceBase(BaseSchema):
    """Base para schemas de preferencia"""
    desired_item_title: str = Field(..., min_length=3, max_length=200, description="Título del item deseado")
    desired_category: Optional[str] = Field(None, max_length=50, description="Categoría deseada")
    min_value: Optional[float] = Field(None, gt=0, description="Valor mínimo aceptable")
    max_value: Optional[float] = Field(None, gt=0, description="Valor máximo aceptable")
    priority: int = Field(default=1, ge=1, le=5, description="Prioridad 1-5")
    is_active: bool = True

class PreferenceCreate(PreferenceBase):
    """Schema para creación de preferencia"""
    item_id: int = Field(..., description="ID del item que se ofrece")

class PreferenceUpdate(BaseSchema):
    """Schema para actualización de preferencia"""
    desired_item_title: Optional[str] = None
    desired_category: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None

class PreferenceResponse(TimestampMixin):
    """Schema para respuesta de preferencia"""
    id: int
    desired_item_title: str
    desired_category: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    priority: int = 1
    is_active: bool = True
    item: ItemResponse
    user: UserResponse

# ============================================================================
# SCHEMAS DE INTERCAMBIO
# ============================================================================

class ExchangeBase(BaseSchema):
    """Base para schemas de intercambio"""
    k_size: int = Field(..., ge=2, le=6, description="Tamaño del ciclo (2-6)")
    total_value: Optional[float] = Field(None, description="Valor total del intercambio")
    expires_at: Optional[datetime] = Field(None, description="Fecha de expiración")

class ExchangeResponse(UUIDMixin, TimestampMixin):
    """Schema para respuesta de intercambio"""
    status: str = "pending"
    k_size: int
    total_value: Optional[float] = None
    commission_total: float = 0.0
    expires_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    participants: List["ExchangeParticipantResponse"]

class ExchangeParticipantBase(BaseSchema):
    """Base para schemas de participante"""
    gives_item_id: int = Field(..., description="ID del item que da")
    receives_item_id: int = Field(..., description="ID del item que recibe")
    monetary_adjustment: float = Field(..., description="Ajuste monetario (+ recibe, - paga)")
    commission: float = Field(default=0.0, description="Comisión Treqe")

class ExchangeParticipantResponse(TimestampMixin):
    """Schema para respuesta de participante"""
    id: int
    status: str = "pending"
    monetary_adjustment: float
    commission: float
    accepted_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    user: UserResponse
    gives_item: ItemResponse
    receives_item: ItemResponse
    exchange: "ExchangeResponse"

# ============================================================================
# SCHEMAS DE MATCHING
# ============================================================================

class MatchingRequest(BaseSchema):
    """Schema para solicitud de matching"""
    k_max: Optional[int] = Field(default=6, ge=2, le=10, description="Tamaño máximo de ciclo a buscar")
    timeout_seconds: Optional[int] = Field(default=300, ge=30, le=600, description="Timeout en segundos")

class MatchingProposal(BaseSchema):
    """Schema para propuesta de matching"""
    exchange: ExchangeResponse
    user_proposal: ExchangeParticipantResponse  # Propuesta específica para este usuario
    other_participants: List[ExchangeParticipantResponse]  # Otros participantes (anonimizados)
    benefits: List[str] = Field(..., description="Beneficios para el usuario")
    action_required: str = Field(..., description="Acción recomendada")

class MatchingResponse(BaseSchema):
    """Schema para respuesta de matching"""
    found_matches: bool
    proposals: List[MatchingProposal] = []
    search_time_seconds: float
    users_in_pool: int
    message: Optional[str] = None

# ============================================================================
# SCHEMAS DE AUTENTICACIÓN
# ============================================================================

class Token(BaseSchema):
    """Schema para token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseSchema):
    """Datos dentro del token JWT"""
    user_id: int
    username: str

# ============================================================================
# SCHEMAS DE ERROR
# ============================================================================

class ErrorResponse(BaseSchema):
    """Schema para respuestas de error"""
    detail: str
    code: Optional[str] = None
    field: Optional[str] = None

class ValidationError(BaseSchema):
    """Schema para errores de validación"""
    loc: List[str]
    msg: str
    type: str

# Resolver referencias circulares
ExchangeResponse.update_forward_refs()
ExchangeParticipantResponse.update_forward_refs()

# Exportar todos los schemas
__all__ = [
    # Usuarios
    "UserCreate", "UserUpdate", "UserLogin", "UserResponse", "UserDetailResponse",
    
    # Items
    "ItemCreate", "ItemUpdate", "ItemResponse",
    
    # Preferencias
    "PreferenceCreate", "PreferenceUpdate", "PreferenceResponse",
    
    # Intercambios
    "ExchangeResponse", "ExchangeParticipantResponse",
    
    # Matching
    "MatchingRequest", "MatchingProposal", "MatchingResponse",
    
    # Autenticación
    "Token", "TokenData",
    
    # Errores
    "ErrorResponse", "ValidationError",
]