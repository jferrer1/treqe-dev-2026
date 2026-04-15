"""
Modelos de base de datos para Treqe
SQLAlchemy ORM models
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    ForeignKey, Text, JSON, DECIMAL, UUID
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    """Modelo de usuario"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    location = Column(String(100))
    reputation_score = Column(DECIMAL(5, 2), default=50.00)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")
    preferences = relationship("Preference", back_populates="user", cascade="all, delete-orphan")
    exchange_participations = relationship("ExchangeParticipant", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

class Item(Base):
    """Modelo de item (oferta)"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), index=True)
    estimated_value = Column(DECIMAL(10, 2), nullable=False)
    condition = Column(String(20))  # new, like_new, good, fair
    photos = Column(JSON)  # URLs de fotos
    status = Column(String(20), default="available")  # available, pending, exchanged
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    owner = relationship("User", back_populates="items")
    preferences = relationship("Preference", back_populates="item", cascade="all, delete-orphan")
    given_exchanges = relationship("ExchangeParticipant", foreign_keys="ExchangeParticipant.gives_item_id", back_populates="gives_item")
    received_exchanges = relationship("ExchangeParticipant", foreign_keys="ExchangeParticipant.receives_item_id", back_populates="receives_item")
    
    def __repr__(self):
        return f"<Item {self.title} (€{self.estimated_value})>"

class Preference(Base):
    """Modelo de preferencia (demanda)"""
    __tablename__ = "preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    desired_item_title = Column(String(200), nullable=False)
    desired_category = Column(String(50), index=True)
    min_value = Column(DECIMAL(10, 2))
    max_value = Column(DECIMAL(10, 2))
    priority = Column(Integer, default=1)  # 1-5
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="preferences")
    item = relationship("Item", back_populates="preferences")
    
    def __repr__(self):
        return f"<Preference {self.user.username} wants {self.desired_item_title}>"

class Exchange(Base):
    """Modelo de intercambio (ciclo completo)"""
    __tablename__ = "exchanges"
    
    id = Column(Integer, primary_key=True, index=True)
    exchange_uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)
    status = Column(String(20), default="pending")  # pending, accepted, completed, cancelled
    k_size = Column(Integer, nullable=False)  # Tamaño ciclo (2-6)
    total_value = Column(DECIMAL(12, 2))
    commission_total = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # Fecha expiración propuesta
    accepted_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relaciones
    participants = relationship("ExchangeParticipant", back_populates="exchange", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Exchange {self.exchange_uuid} (k={self.k_size}, status={self.status})>"

class ExchangeParticipant(Base):
    """Modelo de participante en intercambio"""
    __tablename__ = "exchange_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    gives_item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    receives_item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    monetary_adjustment = Column(DECIMAL(10, 2))  # Positivo si recibe dinero, negativo si paga
    commission = Column(DECIMAL(10, 2), default=0.00)
    status = Column(String(20), default="pending")  # pending, accepted, rejected
    accepted_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    
    # Relaciones
    exchange = relationship("Exchange", back_populates="participants")
    user = relationship("User", back_populates="exchange_participations")
    gives_item = relationship("Item", foreign_keys=[gives_item_id], back_populates="given_exchanges")
    receives_item = relationship("Item", foreign_keys=[receives_item_id], back_populates="received_exchanges")
    
    def __repr__(self):
        return f"<ExchangeParticipant user={self.user_id} exchange={self.exchange_id}>"

class Transaction(Base):
    """Modelo de transacción monetaria"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    transaction_type = Column(String(20))  # payment, receipt, commission, refund
    status = Column(String(20), default="pending")  # pending, completed, failed, refunded
    payment_method = Column(String(50))
    payment_reference = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relaciones
    user = relationship("User")
    exchange = relationship("Exchange")
    
    def __repr__(self):
        return f"<Transaction {self.transaction_uuid} ({self.transaction_type} €{self.amount})>"

class Notification(Base):
    """Modelo de notificación"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    notification_type = Column(String(50))  # match_found, exchange_accepted, etc.
    title = Column(String(200))
    message = Column(Text)
    data = Column(JSON)  # Datos adicionales (exchange_id, etc.)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True))
    
    # Relaciones
    user = relationship("User")
    
    def __repr__(self):
        return f"<Notification {self.notification_type} for user={self.user_id}>"

class SystemLog(Base):
    """Modelo de log del sistema"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20))  # info, warning, error
    component = Column(String(50))  # api, matching, payment, etc.
    message = Column(Text)
    data = Column(JSON)  # Datos adicionales
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<SystemLog {self.level} [{self.component}] {self.message[:50]}...>"

# Índices adicionales para optimización
__all__ = [
    "Base",
    "User", 
    "Item",
    "Preference",
    "Exchange",
    "ExchangeParticipant",
    "Transaction",
    "Notification",
    "SystemLog"
]