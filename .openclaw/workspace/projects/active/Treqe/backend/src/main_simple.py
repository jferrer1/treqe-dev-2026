"""
Treqe Backend - Versión Simplificada para Pruebas
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .database.connection import get_db, init_db
from .api.users_simple import router as users_router
from .api.matching_simple import router as matching_router
from .utils.config import settings
from .utils.logger import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    """
    # Startup
    logger.info("Starting Treqe Backend API (Simplified Version)")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    
    # Inicializar base de datos
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Treqe Backend API")

# Crear aplicación FastAPI
app = FastAPI(
    title="Treqe API (Simplified)",
    description="API simplificada para pruebas de matching",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users_router)
app.include_router(matching_router)

# Health check
@app.get("/")
async def root():
    return {
        "message": "Treqe API (Simplified)",
        "version": "1.0.0",
        "status": "running",
        "database": "SQLite (demo)",
        "endpoints": {
            "users": "/api/v1/users",
            "login": "/api/v1/users/login",
            "register": "/api/v1/users/register"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2026-03-18T22:15:00Z"}

# Info endpoint
@app.get("/info")
async def api_info():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "algorithm": {
            "k_max": settings.TREQE_K_MAX,
            "timeout_seconds": settings.TREQE_TIMEOUT_SECONDS,
            "default_search_k_max": settings.TREQE_DEFAULT_SEARCH_K_MAX,
            "deep_search_k_max": settings.TREQE_DEEP_SEARCH_K_MAX
        },
        "database": settings.DATABASE_URL,
        "commission_rates": {
            "low": f"{settings.COMMISSION_RATE_LOW*100}%",
            "medium": f"{settings.COMMISSION_RATE_MEDIUM*100}%",
            "high": f"{settings.COMMISSION_RATE_HIGH*100}%"
        }
    }