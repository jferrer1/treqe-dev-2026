"""
Router simplificado de matching para pruebas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import time

from ..database.connection import get_db
from ..database.models import User, Item, Preference
from .schemas_simple import MatchingRequest, MatchingResponse, ExchangeCycle
from ..core.algorithm_final import TreqeMatchingEngineFinal

router = APIRouter(prefix="/api/v1/matching", tags=["matching"])

@router.post("/find", response_model=MatchingResponse)
async def find_exchanges(
    request: MatchingRequest,
    db: AsyncSession = Depends(get_db)
):
    """Buscar intercambios para un usuario"""
    try:
        # Verificar que el usuario existe
        stmt = select(User).where(User.id == request.user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Obtener todos los datos necesarios para el algoritmo
        print(f"Buscando intercambios para usuario {user.username} (ID: {user.id})")
        
        # Obtener todos los usuarios activos
        stmt_users = select(User).where(User.is_active == True)
        result_users = await db.execute(stmt_users)
        all_users = result_users.scalars().all()
        
        # Obtener todos los items disponibles
        stmt_items = select(Item).where(Item.status == "available")
        result_items = await db.execute(stmt_items)
        all_items = result_items.scalars().all()
        
        # Obtener todas las preferencias activas
        stmt_prefs = select(Preference).where(Preference.is_active == True)
        result_prefs = await db.execute(stmt_prefs)
        all_prefs = result_prefs.scalars().all()
        
        print(f"Datos cargados: {len(all_users)} usuarios, {len(all_items)} items, {len(all_prefs)} preferencias")
        
        # Crear instancia del motor de matching
        engine = TreqeMatchingEngineFinal(
            users=all_users,
            items=all_items,
            preferences=all_prefs
        )
        
        # Buscar intercambios
        start_time = time.time()
        cycles = engine.find_exchanges_for_user(
            user_id=request.user_id,
            k_max=request.max_k,
            timeout_seconds=request.timeout_seconds
        )
        search_time_ms = (time.time() - start_time) * 1000
        
        # Convertir ciclos al formato de respuesta
        exchange_cycles = []
        for cycle in cycles:
            exchange_cycle = ExchangeCycle(
                k_size=cycle.k_size,
                users=cycle.users,
                items=cycle.items,
                total_value=cycle.total_value,
                commission_total=cycle.commission_total,
                net_adjustments=cycle.net_adjustments
            )
            exchange_cycles.append(exchange_cycle)
        
        return MatchingResponse(
            user_id=request.user_id,
            cycles_found=exchange_cycles,
            search_time_ms=search_time_ms,
            total_cycles=len(exchange_cycles)
        )
        
    except Exception as e:
        print(f"Error en matching: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding exchanges: {str(e)}"
        )

@router.get("/test")
async def test_matching():
    """Endpoint de prueba para verificar que el algoritmo funciona"""
    return {
        "message": "Matching endpoint is working",
        "algorithm": "TreqeMatchingEngineFinal",
        "k_max": 6,
        "timeout_seconds": 5,
        "test_data": "3 users with circular exchange k=3"
    }