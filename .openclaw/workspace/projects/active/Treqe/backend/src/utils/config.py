"""
Configuración de la aplicación Treqe
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Configuración general
    ENVIRONMENT: str = "development"
    APP_NAME: str = "Treqe Backend"
    APP_VERSION: str = "1.0.0"
    
    # Base de datos
    DATABASE_URL: str = "sqlite+aiosqlite:///treqe_demo.db"  # Temporal para pruebas demo
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_POOL_SIZE: int = 10
    
    # Autenticación
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Algoritmo Treqe - Configuración Final Optimizada
    TREQE_K_MAX: int = 6                    # Máximo técnico (k=2→6)
    TREQE_TIMEOUT_SECONDS: int = 5          # 5 segundos máximo (optimizado)
    TREQE_MIN_REPUTATION: int = 30          # Reputación mínima para participar
    
    # Configuración avanzada para algoritmo optimizado
    TREQE_DEFAULT_SEARCH_K_MAX: int = 4     # Búsqueda normal por defecto (k=2→4)
    TREQE_DEEP_SEARCH_K_MAX: int = 6        # Búsqueda profunda opcional (k=2→6)
    TREQE_MAX_USERS_POOL: int = 100         # Máximo usuarios en pool de búsqueda
    TREQE_CACHE_TTL_SECONDS: int = 300      # Cache 5 minutos
    
    # Comisiones
    COMMISSION_RATE_LOW: float = 0.08  # 8% para reputación < 60
    COMMISSION_RATE_MEDIUM: float = 0.06  # 6% para reputación 60-79
    COMMISSION_RATE_HIGH: float = 0.04  # 4% para reputación >= 80
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/treqe.log"
    
    # Email (opcional para desarrollo)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()

# Configuración específica por entorno
if settings.ENVIRONMENT == "production":
    settings.CORS_ORIGINS = [
        "https://app.treqe.com",
        "https://admin.treqe.com",
    ]
    settings.LOG_LEVEL = "WARNING"
    
elif settings.ENVIRONMENT == "staging":
    settings.CORS_ORIGINS = [
        "https://staging.treqe.com",
        "https://admin-staging.treqe.com",
    ]
    settings.LOG_LEVEL = "INFO"
    
elif settings.ENVIRONMENT == "development":
    # Configuración de desarrollo
    settings.CORS_ORIGINS.append("*")  # Permitir todos en desarrollo
    settings.LOG_LEVEL = "DEBUG"

# Validar configuración crítica
def validate_settings():
    """Validar configuración crítica"""
    errors = []
    
    if not settings.SECRET_KEY or settings.SECRET_KEY == "dev-secret-key-change-in-production":
        if settings.ENVIRONMENT == "production":
            errors.append("SECRET_KEY must be set in production environment")
    
    if not settings.DATABASE_URL:
        errors.append("DATABASE_URL must be set")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

# Validar al importar
validate_settings()