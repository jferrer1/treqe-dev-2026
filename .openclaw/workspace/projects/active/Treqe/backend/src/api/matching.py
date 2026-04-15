"""
Endpoints API para matching de intercambios
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import time

from .schemas import MatchingRequest, MatchingResponse, MatchingProposal, ErrorResponse
from .auth import CurrentUser
from ..database.connection import get_db
from ..database.models import User
from ..core.algorithm_final import TreqeMatchingEngineFinal
from ..utils.logger import get_logger

logger = get_logger("api.matching")

router = APIRouter()

# Crear instancia del motor de matching final optimizado
matching_engine_final = TreqeMatchingEngineFinal()

@router.post("/find", response_model=MatchingResponse)
async def find_exchanges(
    matching_request: MatchingRequest,
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Buscar intercambios para el usuario actual
    """
    logger.info(f"Finding exchanges for user {current_user.username}")
    
    start_time = time.time()
    
    try:
        # Buscar intercambios usando el motor de matching FINAL OPTIMIZADO
        exchanges = await matching_engine_final.find_exchanges_for_user(db, current_user.id)
        
        # Convertir a propuestas de matching
        proposals = []
        for exchange in exchanges:
            # Ya está en formato de propuesta del motor de matching
            proposals.append(exchange)
        
        search_time = time.time() - start_time
        
        # Obtener conteo de usuarios en el pool (simplificado para MVP)
        # En producción, esto contaría usuarios activos con items disponibles
        users_in_pool = 50  # Valor por defecto para demostración
        
        response = MatchingResponse(
            found_matches=len(proposals) > 0,
            proposals=proposals,
            search_time_seconds=search_time,
            users_in_pool=users_in_pool,
            message=f"Found {len(proposals)} potential exchange(s)" if proposals else "No exchanges found at this time"
        )
        
        logger.info(f"Matching completed for user {current_user.username}: {len(proposals)} proposals found")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in matching for user {current_user.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching for exchanges"
        )

@router.get("/status")
async def get_matching_status(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener estado del matching para el usuario actual
    """
    logger.debug(f"Getting matching status for user {current_user.username}")
    
    # Obtener conteos básicos
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
    
    # Estadísticas del sistema (simplificado para MVP)
    system_stats = {
        "total_active_users": 150,  # Valor de demostración
        "total_available_items": 420,
        "avg_exchanges_per_day": 12,
        "success_rate": 0.85  # 85% de éxito en intercambios
    }
    
    # Recomendaciones basadas en el perfil del usuario
    recommendations = []
    
    if active_items == 0:
        recommendations.append("Add at least one item to start finding exchanges")
    
    if active_preferences == 0:
        recommendations.append("Add preferences to tell us what items you're looking for")
    
    if active_items >= 5:
        recommendations.append("You have many items! Consider prioritizing which ones you're willing to exchange")
    
    if current_user.reputation_score < 60:
        recommendations.append("Improve your reputation score by completing exchanges successfully")
    
    status_info = {
        "user": {
            "username": current_user.username,
            "active_items": active_items,
            "active_preferences": active_preferences,
            "reputation_score": float(current_user.reputation_score),
            "matching_ready": active_items > 0 and active_preferences > 0
        },
        "system": system_stats,
        "recommendations": recommendations,
        "last_search_time": None,  # Podría almacenarse en base de datos
        "next_recommended_search": "now" if recommendations else "in_24_hours"
    }
    
    return status_info

@router.post("/quick-match")
async def quick_match(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Búsqueda rápida de intercambios (optimizada para velocidad)
    """
    logger.info(f"Quick match for user {current_user.username}")
    
    start_time = time.time()
    
    try:
        # Búsqueda simplificada y rápida
        exchanges = await matching_engine.find_exchanges_for_user(db, current_user.id)
        
        # Para quick-match, usar el motor final pero limitar resultados
        exchanges = await matching_engine_final.find_exchanges_for_user(db, current_user.id)
        
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
            "proposals": quick_results if quick_results else [],
            "message": "Quick match completed" if quick_results else "No quick matches found"
        }
        
    except Exception as e:
        logger.error(f"Error in quick match for user {current_user.username}: {e}")
        return {
            "success": False,
            "error": str(e),
            "found": False,
            "proposals": []
        }

@router.get("/stats/historical")
async def get_historical_stats(
    current_user: User = CurrentUser,
    days: int = Query(30, ge=1, le=365, description="Number of days to look back")
):
    """
    Obtener estadísticas históricas de matching (simplificado para MVP)
    """
    logger.debug(f"Getting historical stats for user {current_user.username}, last {days} days")
    
    # Datos de demostración - en producción esto vendría de la base de datos
    historical_data = {
        "searches_performed": days * 2,  # 2 búsquedas por día en promedio
        "exchanges_found": days,  # 1 intercambio encontrado por día
        "exchanges_accepted": int(days * 0.7),  # 70% tasa de aceptación
        "exchanges_completed": int(days * 0.6),  # 60% tasa de completación
        "total_value_exchanged": days * 500,  # €500 por intercambio en promedio
        "commission_paid": days * 25,  # €25 de comisión por intercambio
        "success_rate": 0.85,  # 85% tasa de éxito
        "avg_search_time_seconds": 2.5,
        "preferences_fulfilled": int(days * 0.8)  # 80% de preferencias cumplidas
    }
    
    # Tendencias (datos de demostración)
    trends = {
        "search_success_trend": "improving",  # improving, stable, declining
        "exchange_value_trend": "increasing",
        "acceptance_rate_trend": "stable",
        "user_satisfaction": "high"  # high, medium, low
    }
    
    # Insights basados en datos históricos
    insights = []
    
    if historical_data["success_rate"] < 0.7:
        insights.append("Consider adjusting your preferences to increase match chances")
    
    if historical_data["exchanges_accepted"] / historical_data["exchanges_found"] < 0.5:
        insights.append("You're rejecting many proposals. Consider being more flexible with values")
    
    if historical_data["avg_search_time_seconds"] > 5:
        insights.append("Searches are taking longer than average. The system may be busy")
    
    return {
        "period_days": days,
        "historical": historical_data,
        "trends": trends,
        "insights": insights,
        "user_comparison": {
            "vs_average_success_rate": "+5%",  # 5% mejor que el promedio
            "vs_average_acceptance": "+10%",
            "vs_average_value": "+15%"
        }
    }

@router.post("/test-match")
async def test_match(
    scenario: str = Query("direct", description="Test scenario: direct, cycle, or complex"),
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Probar matching con diferentes escenarios (solo para desarrollo)
    """
    logger.info(f"Test match for user {current_user.username}, scenario: {scenario}")
    
    # Solo permitir en desarrollo
    from ..utils.config import settings
    if settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Test endpoints are not available in production"
        )
    
    start_time = time.time()
    
    try:
        # Escenarios de prueba predefinidos
        test_proposals = []
        
        if scenario == "direct":
            # Escenario de intercambio directo
            test_proposals.append({
                "title": "Test Direct Exchange: iPhone 13 for MacBook Air M1",
                "summary": "You give iPhone 13 (€600) for MacBook Air M1 (€800)",
                "financial_adjustment": "Pay €212.00 total (€200.00 difference + €12.00 Treqe commission)",
                "benefits": [
                    "You get EXACTLY the MacBook you wanted",
                    "Direct exchange with one other user",
                    "Simple and fast"
                ],
                "recommended_action": "ACCEPT TEST EXCHANGE",
                "net_result": "You give €600 value, receive €800 value, pay €212 = NET: €600",
                "exchange_type": "direct",
                "k_size": 2,
                "is_test": True
            })
        
        elif scenario == "cycle":
            # Escenario de ciclo k=3
            test_proposals.append({
                "title": "Test Cycle Exchange: iPhone → MacBook → Bicicleta → iPhone",
                "summary": "3-user cycle exchange",
                "financial_adjustment": "Pay €212.00 (€200 difference + €12 commission)",
                "benefits": [
                    "Complex exchange that wouldn't be possible with direct trading",
                    "Everyone gets exactly what they want",
                    "Demonstrates Treqe's unique value"
                ],
                "recommended_action": "ACCEPT TEST CYCLE",
                "net_result": "Economic tie, you gain convenience",
                "exchange_type": "cycle",
                "k_size": 3,
                "is_test": True
            })
        
        elif scenario == "complex":
            # Escenario complejo con múltiples opciones
            test_proposals.extend([
                {
                    "title": "Test Option 1: Direct exchange",
                    "summary": "Simple 2-user exchange",
                    "financial_adjustment": "Small adjustment",
                    "benefits": ["Fast", "Simple"],
                    "recommended_action": "ACCEPT",
                    "is_test": True
                },
                {
                    "title": "Test Option 2: Cycle exchange",
                    "summary": "3-user circular exchange",
                    "financial_adjustment": "Moderate adjustment",
                    "benefits": ["Gets exactly what you want", "More complex"],
                    "recommended_action": "ACCEPT",
                    "is_test": True
                },
                {
                    "title": "Test Option 3: Complex exchange",
                    "summary": "4-user multi-cycle exchange",
                    "financial_adjustment": "Multiple adjustments",
                    "benefits": ["Maximum value", "Most complex"],
                    "recommended_action": "ACCEPT",
                    "is_test": True
                }
            ])
        
        search_time = time.time() - start_time
        
        return {
            "scenario": scenario,
            "found": len(test_proposals) > 0,
            "proposals": test_proposals,
            "search_time_seconds": search_time,
            "note": "These are test proposals for development purposes only",
            "user_id": current_user.id,
            "username": current_user.username
        }
        
    except Exception as e:
        logger.error(f"Error in test match: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Test match failed: {str(e)}"
        )

@router.get("/recommendations/improve")
async def get_improvement_recommendations(
    current_user: User = CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener recomendaciones para mejorar las posibilidades de matching
    """
    logger.debug(f"Getting improvement recommendations for user {current_user.username}")
    
    from sqlalchemy import select
    from ..database.models import Item, Preference
    
    # Analizar perfil del usuario
    stmt_items = select(Item).where(
        Item.user_id == current_user.id,
        Item.status == "available"
    )
    result_items = await db.execute(stmt_items)
    user_items = result_items.scalars().all()
    
    stmt_prefs = select(Preference).where(
        Preference.user_id == current_user.id,
        Preference.is_active == True
    )
    result_prefs = await db.execute(stmt_prefs)
    user_preferences = result_prefs.scalars().all()
    
    recommendations = []
    
    # Análisis de items
    if len(user_items) == 0:
        recommendations.append({
            "category": "items",
            "priority": "high",
            "action": "add_item",
            "title": "Add your first item",
            "description": "You need at least one item to start exchanging",
            "details": "Take a photo of an item you're willing to exchange and add it to your profile"
        })
    elif len(user_items) == 1:
        recommendations.append({
            "category": "items",
            "priority": "medium",
            "action": "add_more_items",
            "title": "Add more items",
            "description": "More items increase your chances of finding exchanges",
            "details": "Consider adding 2-3 more items you're willing to exchange"
        })
    
    # Análisis de preferencias
    if len(user_preferences) == 0:
        recommendations.append({
            "category": "preferences",
            "priority": "high",
            "action": "add_preference",
            "title": "Tell us what you want",
            "description": "Add preferences to let us know what items you're looking for",
            "details": "Be specific but not too restrictive. Consider value ranges."
        })
    elif len(user_preferences) < 3:
        recommendations.append({
            "category": "preferences",
            "priority": "medium",
            "action": "diversify_preferences",
            "title": "Diversify your preferences",
            "description": "Different types of preferences increase match possibilities",
            "details": "Add preferences for different categories and value ranges"
        })
    
    # Análisis de valores
    item_values = [float(item.estimated_value) for item in user_items]
    if item_values:
        avg_item_value = sum(item_values) / len(item_values)
        
        if avg_item_value < 100:
            recommendations.append({
                "category": "value",
                "priority": "low",
                "action": "increase_value",
                "title": "Consider higher value items",
                "description": "Higher value items often have more exchange opportunities",
                "details": "You could bundle lower value items or add one higher value item"
            })
        elif avg_item_value > 1000:
            recommendations.append({
                "category": "value",
                "priority": "low",
                "action": "add_lower_value",
                "title": "Add some lower value items",
                "description": "A mix of values increases flexibility",
                "details": "Consider adding items in the €100-300 range"
            })
    
    # Análisis de reputación
    if current_user.reputation_score < 60:
        recommendations.append({
            "category": "reputation",
            "priority": "medium",
            "action": "improve_reputation",
            "title": "Improve your reputation score",
            "description": "Higher reputation means lower commissions and more trust",
            "details": "Complete exchanges successfully, respond promptly, be reliable"
        })
    
    # Categorizar por prioridad
    high_priority = [r for r in recommendations if r["priority"] == "high"]
    medium_priority = [r for r in recommendations if r["priority"] == "medium"]
    low_priority = [r for r in recommendations if r["priority"] == "low"]
    
    return {
        "user_analysis": {
            "items_count": len(user_items),
            "preferences_count": len(user_preferences),
            "reputation_score": float(current_user.reputation_score),
            "avg_item_value": avg_item_value if item_values else 0
        },
        "recommendations": {
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority
        },
        "estimated_impact": {
            "with_all_changes": "70% increase in match chances",
            "with_high_priority": "40% increase in match chances",
            "time_to_implement": "15-30 minutes"
        }
    }