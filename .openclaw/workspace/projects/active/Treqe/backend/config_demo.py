"""
Configuración demo para Treqe - Usa SQLite
"""

class Settings:
    # Configuración general
    ENVIRONMENT = "development"
    APP_NAME = "Treqe Backend"
    APP_VERSION = "1.0.0"
    
    # Base de datos SQLite
    DATABASE_URL = "sqlite+aiosqlite:///treqe_demo.db"
    DATABASE_POOL_SIZE = 5
    DATABASE_MAX_OVERFLOW = 10
    
    # Redis (no necesario para demo)
    REDIS_URL = "redis://localhost:6379/0"
    REDIS_POOL_SIZE = 10
    
    # Autenticación
    SECRET_KEY = "demo-secret-key-for-testing-only"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8000", "*"]
    
    # Algoritmo Treqe
    TREQE_K_MAX = 6
    TREQE_TIMEOUT_SECONDS = 5
    TREQE_MIN_REPUTATION = 30
    
    # Comisiones
    COMMISSION_RATE_LOW = 0.08    # 8% para reputación < 60
    COMMISSION_RATE_MEDIUM = 0.06 # 6% para reputación 60-79
    COMMISSION_RATE_HIGH = 0.04   # 4% para reputación >= 80
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/treqe_demo.log"

settings = Settings()