"""
Treqe Backend - API Principal
FastAPI application con algoritmo de matching circular
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging

from .database.connection import get_db, init_db
from .api import users, items, preferences, matching, proposals
from .utils.config import settings
from .utils.logger import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Esquema de autenticación
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    """
    # Startup
    logger.info("Starting Treqe Backend API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
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
    title="Treqe API",
    description="API para matching de intercambios circulares",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
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

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Endpoint de health check para monitoreo
    """
    return {
        "status": "healthy",
        "service": "treqe-api",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

# Endpoint de información del sistema
@app.get("/")
async def root():
    """
    Endpoint raíz con información del sistema
    """
    return {
        "message": "Welcome to Treqe API",
        "description": "Circular exchange matching platform",
        "version": "1.0.0",
        "docs": "/docs" if settings.ENVIRONMENT != "production" else None,
        "health": "/health"
    }

# Incluir routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(preferences.router, prefix="/api/v1/preferences", tags=["preferences"])
app.include_router(matching.router, prefix="/api/v1/matching", tags=["matching"])
app.include_router(proposals.router, prefix="/api/v1/proposals", tags=["proposals"])

# Handler para errores 404
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return {
        "detail": "Endpoint not found",
        "path": request.url.path,
        "available_endpoints": [
            "/api/v1/users/",
            "/api/v1/items/",
            "/api/v1/preferences/",
            "/api/v1/matching/",
            "/api/v1/proposals/",
            "/health",
            "/docs"
        ]
    }

# Handler para errores 500
@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return {
        "detail": "Internal server error",
        "message": "An unexpected error occurred. Please try again later."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )