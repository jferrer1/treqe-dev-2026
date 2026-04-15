"""
Conexión a base de datos PostgreSQL para Treqe
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator
import asyncio

from .models import Base
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger("database")

# Crear engine asíncrono para PostgreSQL
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # Echo SQL en desarrollo
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    pool_recycle=3600,   # Reciclar conexiones cada hora
)

# Session factory asíncrona
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Obtener sesión de base de datos para inyección de dependencias
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def init_db():
    """
    Inicializar base de datos (crear tablas si no existen)
    """
    logger.info("Initializing database...")
    
    async with engine.begin() as conn:
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
        
        # Verificar conexión
        try:
            # Para SQLite, usar SELECT sqlite_version()
            if "sqlite" in settings.DATABASE_URL:
                result = await conn.execute(text("SELECT sqlite_version()"))
                version = result.scalar()
                logger.info(f"Connected to SQLite: {version}")
            else:
                result = await conn.execute(text("SELECT version()"))
                version = result.scalar()
                logger.info(f"Connected to PostgreSQL: {version}")
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            # No lanzar excepción para SQLite en pruebas
    
    logger.info("Database initialization complete")

async def check_db_health() -> bool:
    """
    Verificar salud de la base de datos
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            health_check = result.scalar() == 1
            logger.debug("Database health check: OK")
            return health_check
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

async def close_db():
    """
    Cerrar conexiones de base de datos
    """
    logger.info("Closing database connections...")
    await engine.dispose()
    logger.info("Database connections closed")

# Funciones de utilidad para transacciones
class DatabaseTransaction:
    """Context manager para transacciones de base de datos"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
            await self.session.close()

# Métodos CRUD base
class BaseCRUD:
    """Clase base para operaciones CRUD"""
    
    def __init__(self, model):
        self.model = model
    
    async def create(self, db: AsyncSession, **kwargs):
        """Crear nuevo registro"""
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get(self, db: AsyncSession, id: int):
        """Obtener registro por ID"""
        return await db.get(self.model, id)
    
    async def get_by_uuid(self, db: AsyncSession, uuid: str):
        """Obtener registro por UUID"""
        from sqlalchemy import select
        stmt = select(self.model).where(self.model.uuid == uuid)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100, **filters):
        """Obtener múltiples registros con filtros"""
        from sqlalchemy import select
        stmt = select(self.model)
        
        # Aplicar filtros
        for key, value in filters.items():
            if hasattr(self.model, key):
                if value is not None:
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, db_obj, **kwargs):
        """Actualizar registro"""
        for key, value in kwargs.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int):
        """Eliminar registro"""
        db_obj = await self.get(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

# Exportar funciones principales
__all__ = [
    "engine",
    "AsyncSessionLocal",
    "get_db",
    "init_db",
    "check_db_health",
    "close_db",
    "DatabaseTransaction",
    "BaseCRUD",
]