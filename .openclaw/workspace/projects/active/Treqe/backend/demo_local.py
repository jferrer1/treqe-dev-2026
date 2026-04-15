"""
Treqe Demo Local - Versión ultra simple solo para localhost
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import os

# Configuración
DATABASE_PATH = "treqe_demo.db"

# Verificar que existe la base de datos
if not os.path.exists(DATABASE_PATH):
    print(f"ERROR: No se encuentra {DATABASE_PATH}")
    print("Ejecuta primero: python crear_datos_final.py")
    exit(1)

# Crear aplicación FastAPI
app = FastAPI(
    title="Treqe Demo Local",
    description="Demo privada solo para localhost",
    version="0.1.0"
)

# Configurar CORS solo para localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Obtener conexión a SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Treqe Demo API - Solo localhost",
        "version": "0.1.0",
        "status": "running",
        "access": "private"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "database": "connected"}

@app.get("/api/v1/users")
async def get_users():
    """Obtener usuarios demo"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email, created_at FROM users")
    users = cursor.fetchall()
    
    conn.close()
    
    return {
        "users": [dict(user) for user in users],
        "count": len(users)
    }

@app.post("/api/v1/users/login")
async def login(username: str, password: str):
    """Login simplificado (solo para demo)"""
    # En demo real usaríamos bcrypt
    if username == "ana_tech" and password == "password123":
        return {
            "success": True,
            "user": {
                "id": 1,
                "username": "ana_tech",
                "email": "ana@example.com"
            },
            "token": "demo_token_123"
        }
    elif username == "carlos_deportes" and password == "password123":
        return {
            "success": True,
            "user": {
                "id": 2,
                "username": "carlos_deportes",
                "email": "carlos@example.com"
            },
            "token": "demo_token_456"
        }
    elif username == "beatriz_eco" and password == "password123":
        return {
            "success": True,
            "user": {
                "id": 3,
                "username": "beatriz_eco",
                "email": "beatriz@example.com"
            },
            "token": "demo_token_789"
        }
    
    return {"success": False, "error": "Credenciales incorrectas"}

@app.get("/api/v1/matching/find/{user_id}")
async def find_matches(user_id: int):
    """Encontrar intercambios para un usuario"""
    # Simulación simple del algoritmo
    if user_id == 1:  # Ana
        return {
            "user_id": 1,
            "username": "ana_tech",
            "matches": [
                {
                    "cycle": [
                        {"user_id": 1, "username": "ana_tech", "item_gives": "iPhone 13", "item_receives": "MacBook Air"},
                        {"user_id": 2, "username": "carlos_deportes", "item_gives": "MacBook Air", "item_receives": "Bicicleta"},
                        {"user_id": 3, "username": "beatriz_eco", "item_gives": "Bicicleta", "item_receives": "iPhone 13"}
                    ],
                    "financial_summary": {
                        "ana_pays": 208.0,
                        "carlos_receives": 376.0,
                        "beatriz_pays": 212.0,
                        "total_commissions": 44.0
                    },
                    "probability": 0.95
                }
            ]
        }
    elif user_id == 2:  # Carlos
        return {
            "user_id": 2,
            "username": "carlos_deportes",
            "matches": [
                {
                    "cycle": [
                        {"user_id": 2, "username": "carlos_deportes", "item_gives": "MacBook Air", "item_receives": "Bicicleta"},
                        {"user_id": 3, "username": "beatriz_eco", "item_gives": "Bicicleta", "item_receives": "iPhone 13"},
                        {"user_id": 1, "username": "ana_tech", "item_gives": "iPhone 13", "item_receives": "MacBook Air"}
                    ],
                    "financial_summary": {
                        "carlos_receives": 376.0,
                        "beatriz_pays": 212.0,
                        "ana_pays": 208.0,
                        "total_commissions": 44.0
                    },
                    "probability": 0.95
                }
            ]
        }
    elif user_id == 3:  # Beatriz
        return {
            "user_id": 3,
            "username": "beatriz_eco",
            "matches": [
                {
                    "cycle": [
                        {"user_id": 3, "username": "beatriz_eco", "item_gives": "Bicicleta", "item_receives": "iPhone 13"},
                        {"user_id": 1, "username": "ana_tech", "item_gives": "iPhone 13", "item_receives": "MacBook Air"},
                        {"user_id": 2, "username": "carlos_deportes", "item_gives": "MacBook Air", "item_receives": "Bicicleta"}
                    ],
                    "financial_summary": {
                        "beatriz_pays": 212.0,
                        "ana_pays": 208.0,
                        "carlos_receives": 376.0,
                        "total_commissions": 44.0
                    },
                    "probability": 0.95
                }
            ]
        }
    
    return {"user_id": user_id, "matches": [], "error": "Usuario no encontrado"}

@app.get("/api/v1/items")
async def get_items():
    """Obtener items demo"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT i.id, i.title, i.description, i.value, i.category, 
               u.username as owner_username
        FROM items i
        JOIN users u ON i.owner_id = u.id
    """)
    items = cursor.fetchall()
    
    conn.close()
    
    return {
        "items": [dict(item) for item in items],
        "count": len(items)
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("TREQE DEMO LOCAL - SOLO LOCALHOST")
    print("=" * 60)
    print("URL: http://localhost:8000")
    print("Health: http://localhost:8000/health")
    print("Login demo: ana_tech / password123")
    print("=" * 60)
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # Solo aceptar conexiones locales
    uvicorn.run(
        app, 
        host="127.0.0.1",  # Solo localhost
        port=8000,
        log_level="info"
    )