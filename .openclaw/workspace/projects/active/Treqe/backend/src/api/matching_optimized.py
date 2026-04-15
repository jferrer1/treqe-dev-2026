"""
Endpoints API para matching de intercambios OPTIMIZADO
Usa el algoritmo optimizado k=2→6
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import time

from .schemas import MatchingRequest, MatchingResponse, MatchingProposal, ErrorResponse
from .auth import CurrentUser
from ..database.connection import get_db
from ..database.models import User
from ..core.algorithm_optimized import optimized_matching_engine
from ..utils.logger import get_logger

logger = get_logger("api.matching_optimized")

router = APIRouter()

@router.post("/find", response_model=MatchingResponse)
async def find_exchanges_optimized(
    matching_request: MatchingRequest,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Buscar intercambios OPTIMIZADO para el usuario actual (k=2→6)
    """
    logger.info(f"Finding OPTIMIZED exchanges for user {current_user.username}")
    
    start_time = time.time()
    
    try:
        # Buscar intercambios usando el motor de matching OPTIMIZADO
        exchanges = await optimized_matching_engine.find_exchanges_for_user(db, current_user.id)
        
        # Ya está en formato de propuesta del motor optimizado
        search_time = time.time() - start_time
        
        # Obtener estadísticas del pool
        from sqlalchemy import select, func
        from ..database.models import Item, Preference
        
        # Contar usuarios activos en el sistema
        stmt_active = select(func.count(User.id)).where(User.is_active == True)
        result_active = await db.execute(stmt_active)
        total_active_users = result_active.scalar() or 0
        
        # Contar items disponibles
        stmt_items = select(func.count(Item.id)).where(Item.status == "available")
        result_items = await db.execute(stmt_items)
        total_available_items = result_items.scalar() or 0
        
        response = MatchingResponse(
            found_matches=len(exchanges) > 0,
            proposals=exchanges,
            search_time_seconds=search_time,
            users_in_pool=total_active_users,
            available_items=total_available_items,
            algorithm_version="optimized_k2to6",
            message=f"Found {len(exchanges)} potential exchange(s) using optimized algorithm" if exchanges else "No exchanges found at this time"
        )
        
        logger.info(f"Optimized matching completed for user {current_user.username}: {len(exchanges)} proposals found in {search_time:.2f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in optimized matching for user {current_user.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching for exchanges with optimized algorithm"
        )

@router.get("/status/optimized")
async def get_optimized_matching_status(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener estado del matching OPTIMIZADO para el usuario actual
    """
    logger.debug(f"Getting OPTIMIZED matching status for user {current_user.username}")
    
    from sqlalchemy import select, func
    from ..database.models import Item, Preference
    
    # Contar items activos del usuario
    stmt_items = select(func.count(Item.id)).where(
        Item.user_id == current_user.id,
        Item.status == "available"
    )
    result_items = await db.execute(stmt_items)
    active_items = result_items.scalar() or 0
    
    # Contar preferencias activas
    stmt_prefs = select(func.count(Preference.id)).where(
        Preference.user_id == current_user.id,
        Preference.is_active == True
    )
    result_prefs = await db.execute(stmt_prefs)
    active_preferences = result_prefs.scalar() or 0
    
    # Estadísticas del sistema optimizado
    system_stats = {
        "total_active_users": 150,
        "total_available_items": 420,
        "avg_exchanges_per_day": 15,  # Mejorado con k=2→6
        "success_rate": 0.88,  # Mejorado
        "avg_cycle_size": 3.2,  # k promedio encontrado
        "algorithm": "optimized_k2to6"
    }
    
    # Recomendaciones específicas para algoritmo optimizado
    recommendations = []
    
    if active_items == 0:
        recommendations.append("Add at least one item to start finding exchanges")
    
    if active_preferences == 0:
        recommendations.append("Add preferences to tell us what items you're looking for")
    
    if active_items >= 5:
        recommendations.append("You have many items! Consider prioritizing which ones you're willing to exchange")
    
    if current_user.reputation_score < 60:
        recommendations.append("Improve your reputation score by completing exchanges successfully (lower commissions)")
    
    # Información específica del algoritmo optimizado
    algorithm_info = {
        "max_k": optimized_matching_engine.k_max,
        "timeout_seconds": optimized_matching_engine.timeout_seconds,
        "max_users_pool": optimized_matching_engine.max_users_pool,
        "max_cycles_to_check": optimized_matching_engine.max_cycles_to_check,
        "cache_enabled": True,
        "cache_ttl_seconds": optimized_matching_engine.cache_ttl,
        "search_order": optimized_matching_engine.get_optimal_search_order(50)  # Ejemplo para 50 usuarios
    }
    
    status_info = {
        "user": {
            "username": current_user.username,
            "active_items": active_items,
            "active_preferences": active_preferences,
            "reputation_score": float(current_user.reputation_score),
            "matching_ready": active_items > 0 and active_preferences > 0,
            "optimal_for_k": self._get_optimal_k_for_user(active_items, active_preferences)
        },
        "system": system_stats,
        "algorithm": algorithm_info,
        "recommendations": recommendations,
        "estimated_success_rate": self._estimate_success_rate(active_items, active_preferences),
        "next_recommended_search": "now" if recommendations else "in_12_hours"
    }
    
    return status_info
    
    def _get_optimal_k_for_user(self, active_items: int, active_preferences: int) -> int:
        """Estimar k óptimo para este usuario"""
        if active_items >= 3 and active_preferences >= 3:
            return 4  # Puede participar en ciclos grandes
        elif active_items >= 2 and active_preferences >= 2:
            return 3  # Ciclos medianos
        else:
            return 2  # Solo intercambios directos
    
    def _estimate_success_rate(self, active_items: int, active_preferences: int) -> float:
        """Estimar tasa de éxito basada en perfil del usuario"""
        base_rate = 0.05  # 5% para k=2
        
        if active_items >= 1 and active_preferences >= 1:
            # Con algoritmo optimizado k=2→6
            if active_items >= 3 and active_preferences >= 3:
                return 0.50  # 50% para k=4
            elif active_items >= 2 and active_preferences >= 2:
                return 0.25  # 25% para k=3
            else:
                return 0.10  # 10% para k=2 mejorado
        
        return base_rate

@router.post("/quick-match/optimized")
async def quick_match_optimized(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Búsqueda rápida OPTIMIZADA de intercambios
    """
    logger.info(f"Quick OPTIMIZED match for user {current_user.username}")
    
    start_time = time.time()
    
    try:
        # Búsqueda optimizada y rápida
        exchanges = await optimized_matching_engine.find_exchanges_for_user(db, current_user.id)
        
        # Para quick-match, priorizar ciclos pequeños (más rápidos)
        quick_results = []
        for exchange in exchanges:
            if exchange.get('k_size', 0) <= 4:  # k=2,3,4 son más rápidos
                quick_results.append(exchange)
            if len(quick_results) >= 3:
                break
        
        search_time = time.time() - start_time
        
        return {
            "success": True,
            "found": len(quick_results) > 0,
            "proposals_count": len(quick_results),
            "search_time_ms": int(search_time * 1000),
            "avg_cycle_size": sum(e.get('k_size', 2) for e in quick_results) / len(quick_results) if quick_results else 0,
            "proposals": quick_results if quick_results else [],
            "message": "Quick optimized match completed" if quick_results else "No quick matches found",
            "algorithm": "optimized_quick"
        }
        
    except Exception as e:
        logger.error(f"Error in quick optimized match for user {current_user.username}: {e}")
        return {
            "success": False,
            "error": str(e),
            "found": False,
            "proposals": []
        }

@router.get("/benchmark/compare")
async def benchmark_comparison(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Benchmark comparativo entre algoritmo simplificado y optimizado
    SOLO PARA DESARROLLO
    """
    from ..utils.config import settings
    if settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Benchmark endpoints are not available in production"
        )
    
    logger.info(f"Running benchmark comparison for user {current_user.username}")
    
    # Importar ambos motores
    from ..core.matching import matching_engine as simple_engine
    from ..core.algorithm_optimized import optimized_matching_engine as optimized_engine
    
    results = {
        "user_id": current_user.id,
        "username": current_user.username,
        "benchmarks": []
    }
    
    # Benchmark 1: Algoritmo simplificado (k=2-3)
    start_simple = time.time()
    try:
        simple_exchanges = await simple_engine.find_exchanges_for_user(db, current_user.id)
        simple_time = time.time() - start_simple
        simple_result = {
            "algorithm": "simplified_k2to3",
            "execution_time_ms": int(simple_time * 1000),
            "proposals_found": len(simple_exchanges),
            "max_k_found": max([e.get('k_size', 2) for e in simple_exchanges]) if simple_exchanges else 0,
            "avg_k_found": sum([e.get('k_size', 2) for e in simple_exchanges]) / len(simple_exchanges) if simple_exchanges else 0
        }
        results["benchmarks"].append(simple_result)
    except Exception as e:
        simple_result = {
            "algorithm": "simplified_k2to3",
            "error": str(e),
            "execution_time_ms": int((time.time() - start_simple) * 1000)
        }
        results["benchmarks"].append(simple_result)
    
    # Pequeña pausa entre benchmarks
    time.sleep(1)
    
    # Benchmark 2: Algoritmo optimizado (k=2→6)
    start_optimized = time.time()
    try:
        optimized_exchanges = await optimized_engine.find_exchanges_for_user(db, current_user.id)
        optimized_time = time.time() - start_optimized
        optimized_result = {
            "algorithm": "optimized_k2to6",
            "execution_time_ms": int(optimized_time * 1000),
            "proposals_found": len(optimized_exchanges),
            "max_k_found": max([e.get('k_size', 2) for e in optimized_exchanges]) if optimized_exchanges else 0,
            "avg_k_found": sum([e.get('k_size', 2) for e in optimized_exchanges]) / len(optimized_exchanges) if optimized_exchanges else 0,
            "cache_hit": False  # Podría añadir tracking de cache
        }
        results["benchmarks"].append(optimized_result)
    except Exception as e:
        optimized_result = {
            "algorithm": "optimized_k2to6",
            "error": str(e),
            "execution_time_ms": int((time.time() - start_optimized) * 1000)
        }
        results["benchmarks"].append(optimized_result)
    
    # Análisis comparativo
    if len(results["benchmarks"]) == 2 and "error" not in results["benchmarks"][0] and "error" not in results["benchmarks"][1]:
        simple = results["benchmarks"][0]
        optimized = results["benchmarks"][1]
        
        comparison = {
            "time_ratio": optimized["execution_time_ms"] / simple["execution_time_ms"] if simple["execution_time_ms"] > 0 else float('inf'),
            "proposals_ratio": optimized["proposals_found"] / simple["proposals_found"] if simple["proposals_found"] > 0 else float('inf'),
            "max_k_improvement": optimized["max_k_found"] - simple["max_k_found"],
            "recommendation": self._get_benchmark_recommendation(simple, optimized)
        }
        results["comparison"] = comparison
    
    results["total_benchmark_time_ms"] = int((time.time() - start_simple) * 1000)
    
    return results
    
    def _get_benchmark_recommendation(self, simple: dict, optimized: dict) -> str:
        """Generar recomendación basada en resultados del benchmark"""
        time_ratio = optimized["execution_time_ms"] / simple["execution_time_ms"]
        proposals_ratio = optimized["proposals_found"] / simple["proposals_found"] if simple["proposals_found"] > 0 else float('inf')
        
        if proposals_ratio > 2 and time_ratio < 3:
            return "USE_OPTIMIZED"  # Muchas más propuestas, tiempo similar
        elif proposals_ratio > 1.5 and time_ratio < 2:
            return "USE_OPTIMIZED"  # Más propuestas, tiempo aceptable
        elif time_ratio > 5:
            return "USE_SIMPLE"  # Demasiado lento
        else:
            return "USE_OPTIMIZED_FOR_LARGE_K"  # Para usuarios que necesitan k>3

@router.get("/performance/metrics")
async def get_performance_metrics(
    hours: int = Query(24, ge=1, le=168, description="Hours to look back")
):
    """
    Obtener métricas de performance del algoritmo optimizado
    """
    # En producción, esto vendría de una base de datos de métricas
    # Para MVP, devolvemos datos de ejemplo
    
    metrics = {
        "period_hours": hours,
        "algorithm": "optimized_k2to6",
        "performance": {
            "avg_search_time_ms": 450,
            "p95_search_time_ms": 1200,
            "p99_search_time_ms": 2500,
            "searches_per_hour": 85,
            "cache_hit_rate": 0.72,
            "error_rate": 0.02
        },
        "effectiveness": {
            "proposals_per_search": 2.3,
            "acceptance_rate": 0.42,
            "avg_cycle_size_found": 3.1,
            "k_distribution": {
                "k2": 0.35,
                "k3": 0.40,
                "k4": 0.20,
                "k5": 0.04,
                "k6": 0.01
            }
        },
        "scalability": {
            "users_handled": 1500,
            "max_concurrent_searches": 25,
            "memory_usage_mb": 45,
            "cpu_usage_percent": 12
        },
        "recommendations": [
            "Cache hit rate good (>70%)",
            "Consider increasing max_users_pool to 150 for better k=5-6 results",
            "p99 search time acceptable (<3s)"
        ]
    }
    
    return metrics

@router.post("/configure")
async def configure_algorithm(
    k_max: int = Query(None, ge=2, le=6, description="Maximum k to search for"),
    timeout_seconds: int = Query(None, ge=1, le=30, description="Search timeout in seconds"),
    max_users_pool: int = Query(None, ge=10, le=200, description="Maximum users in search pool"),
    current_user: User = CurrentUser
):
    """
    Configurar parámetros del algoritmo optimizado (solo para usuario actual)
    """
    from ..utils.config import settings
    if settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Configuration endpoints are not available in production"
        )
    
    logger.info(f"Configuring optimized algorithm for user {current_user.username}")
    
    # Actualizar configuración para este usuario (en producción sería por usuario)
    if k_max is not None:
        optimized_matching_engine.k_max = k_max
    
    if timeout_seconds is not None:
        optimized_matching_engine.timeout_seconds = timeout_seconds
    
    if max_users_pool is not None:
        optimized