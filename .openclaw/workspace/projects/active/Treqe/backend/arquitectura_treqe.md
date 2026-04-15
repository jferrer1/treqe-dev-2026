# ARQUITECTURA BACKEND TREQE

## 🎯 OBJETIVO
Sistema backend escalable para matching de intercambios circulares con lógica económica correcta.

## 📁 ESTRUCTURA DE DIRECTORIOS
```
treqe_backend/
├── src/
│   ├── api/              # API REST endpoints
│   │   ├── __init__.py
│   │   ├── users.py      # Gestión usuarios
│   │   ├── items.py      # Gestión items
│   │   ├── matching.py   # Endpoints matching
│   │   └── proposals.py  # Propuestas intercambio
│   ├── core/             # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── algorithm.py  # Algoritmo Treqe corregido
│   │   ├── economics.py  # Lógica económica
│   │   ├── matching.py   # Matching engine
│   │   └── validation.py # Validación datos
│   ├── database/         # Base de datos
│   │   ├── __init__.py
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── crud.py       # Operaciones CRUD
│   │   └── connection.py # Conexión DB
│   ├── services/         # Servicios externos
│   │   ├── __init__.py
│   │   ├── notifications.py # Notificaciones push/email
│   │   ├── payments.py   # Integración pagos
│   │   └── messaging.py  # Mensajería interna
│   └── utils/            # Utilidades
│       ├── __init__.py
│       ├── config.py     # Configuración
│       ├── logger.py     # Logging estructurado
│       └── helpers.py    # Funciones helper
├── tests/                # Tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_algorithm.py
│   └── test_economics.py
├── migrations/           # Migraciones DB
├── docker/              # Docker config
├── requirements.txt     # Dependencias
├── .env.example        # Variables entorno
├── docker-compose.yml  # Orquestación
└── README.md           # Documentación
```

## 🗄️ MODELO DE DATOS

### **USUARIOS**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    location VARCHAR(100),
    reputation_score DECIMAL(5,2) DEFAULT 50.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **ITEMS (OFERTAS)**
```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    estimated_value DECIMAL(10,2) NOT NULL,
    condition VARCHAR(20), -- new, like_new, good, fair
    photos JSONB, -- URLs de fotos
    status VARCHAR(20) DEFAULT 'available', -- available, pending, exchanged
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **PREFERENCIAS (DEMANDAS)**
```sql
CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    item_id INTEGER REFERENCES items(id), -- Item que ofrece
    desired_item_title VARCHAR(200) NOT NULL,
    desired_category VARCHAR(50),
    min_value DECIMAL(10,2),
    max_value DECIMAL(10,2),
    priority INTEGER DEFAULT 1, -- 1-5
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **INTERCAMBIOS**
```sql
CREATE TABLE exchanges (
    id SERIAL PRIMARY KEY,
    exchange_uuid UUID UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, completed, cancelled
    k_size INTEGER NOT NULL, -- Tamaño ciclo (2-6)
    total_value DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP, -- Fecha expiración propuesta
    completed_at TIMESTAMP
);
```

### **PARTICIPANTES INTERCAMBIO**
```sql
CREATE TABLE exchange_participants (
    id SERIAL PRIMARY KEY,
    exchange_id INTEGER REFERENCES exchanges(id),
    user_id INTEGER REFERENCES users(id),
    gives_item_id INTEGER REFERENCES items(id),
    receives_item_id INTEGER REFERENCES items(id),
    monetary_adjustment DECIMAL(10,2), -- Positivo si recibe dinero, negativo si paga
    commission DECIMAL(10,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, rejected
    accepted_at TIMESTAMP,
    INDEX idx_exchange_user (exchange_id, user_id)
);
```

## 🔌 API ENDPOINTS

### **USUARIOS**
```
POST   /api/v1/users/register     # Registrar usuario
POST   /api/v1/users/login        # Login
GET    /api/v1/users/me           # Perfil propio
PUT    /api/v1/users/me           # Actualizar perfil
GET    /api/v1/users/{id}         # Ver perfil (público)
```

### **ITEMS**
```
POST   /api/v1/items              # Crear item
GET    /api/v1/items              # Listar items (con filtros)
GET    /api/v1/items/{id}         # Ver item detalle
PUT    /api/v1/items/{id}         # Actualizar item
DELETE /api/v1/items/{id}         # Eliminar item
```

### **PREFERENCIAS**
```
POST   /api/v1/preferences        # Añadir preferencia
GET    /api/v1/preferences        # Listar preferencias usuario
DELETE /api/v1/preferences/{id}   # Eliminar preferencia
```

### **MATCHING**
```
POST   /api/v1/matching/find      # Buscar intercambios para usuario
GET    /api/v1/matching/status    # Estado matching usuario
POST   /api/v1/matching/accept    # Aceptar intercambio
POST   /api/v1/matching/reject    # Rechazar intercambio
```

### **PROPUESTAS**
```
GET    /api/v1/proposals          # Listar propuestas activas
GET    /api/v1/proposals/{id}     # Ver propuesta detalle
POST   /api/v1/proposals/{id}/action  # Acción sobre propuesta
```

## 🔧 ALGORITMO INTEGRADO

### **FLUJO DE MATCHING:**
```python
class TreqeMatchingEngine:
    def find_exchanges_for_user(self, user_id: int, k_max: int = 6):
        """
        1. Obtener items y preferencias usuario
        2. Construir grafo de preferencias
        3. Buscar ciclos k=2 → k_max
        4. Calcular compensaciones económicas
        5. Generar propuestas claras
        6. Retornar mejores opciones
        """
    
    def calculate_economic_adjustments(self, cycle: List[User]):
        """
        Implementa lógica económica correcta:
        - Quien recibe item de MAYOR valor → PAGA diferencia
        - Quien da item de MAYOR valor → RECIBE diferencia
        - Comisiones transparentes (4-8%)
        - Sistema cerrado: total dinero = 0
        """
```

### **PROCESAMIENTO ASÍNCRONO:**
```python
# Usar Celery + Redis para procesamiento pesado
@celery.task
def async_find_matches(user_id: int):
    """Ejecutar matching en background"""
    engine = TreqeMatchingEngine()
    matches = engine.find_exchanges_for_user(user_id)
    
    # Guardar resultados
    save_matches_to_db(user_id, matches)
    
    # Enviar notificación
    send_match_notification(user_id, matches)
```

## 💰 SISTEMA ECONÓMICO

### **COMISIONES:**
```python
def calculate_commission(user_reputation: float, amount: float) -> float:
    """
    Comisiones escalonadas por reputación:
    - < 60 puntos: 8%
    - 60-79 puntos: 6%
    - >= 80 puntos: 4%
    """
    if user_reputation < 60:
        rate = 0.08
    elif user_reputation < 80:
        rate = 0.06
    else:
        rate = 0.04
    
    return amount * rate
```

### **GARANTÍAS:**
- **Fondo garantía:** 5% de cada transacción exitosa
- **Seguro envíos:** Opcional (2-3% adicional)
- **Disputas:** Sistema de mediación integrado
- **Reputación:** Sistema de scoring basado en transacciones

## 🚀 DESPLIEGUE

### **STACK TECNOLÓGICO:**
- **Backend:** FastAPI (Python 3.11+)
- **Base datos:** PostgreSQL + Redis (cache/cola)
- **ORM:** SQLAlchemy + Alembic (migraciones)
- **Autenticación:** JWT + OAuth2
- **Colas:** Celery + Redis
- **Contenedores:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana

### **ESCALABILIDAD:**
```yaml
# docker-compose.yml
services:
  api:
    image: treqe-api:latest
    scale: 3  # 3 instancias API
    depends_on:
      - postgres
      - redis
  
  matching-worker:
    image: treqe-matching:latest
    scale: 2  # 2 workers matching
    command: celery -A src.tasks worker -l info -Q matching
  
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
```

## 📊 MONITORING & ANALYTICS

### **MÉTRICAS CLAVE:**
- **Tasa matching:** % usuarios con intercambios encontrados
- **Tasa aceptación:** % propuestas aceptadas
- **Tiempo matching:** Promedio segundos por búsqueda
- **Valor intercambiado:** EUR total en intercambios
- **Comisiones:** Ingresos por comisiones
- **Satisfacción:** Rating usuarios (1-5 estrellas)

### **DASHBOARD ADMIN:**
- **Overview:** Métricas principales
- **Usuarios:** Crecimiento, actividad
- **Intercambios:** Volumen, valor, éxito
- **Problemas:** Disputas, rechazos, cancelaciones
- **Performance:** Tiempos respuesta, errores

## 🔒 SEGURIDAD

### **AUTENTICACIÓN:**
- JWT con refresh tokens
- Rate limiting por IP/usuario
- 2FA opcional para transacciones grandes

### **DATOS:**
- Encriptación en tránsito (TLS 1.3)
- Encriptación en reposo (AES-256)
- PII anonimizada para analytics
- Backups automáticos diarios

### **PAGOS:**
- Stripe Connect para manejo fondos
- Escrow automático para garantías
- Auditoría completa transacciones

## 🧪 TESTING

### **TESTS UNITARIOS:**
```python
def test_economic_logic_correct():
    """Verificar lógica económica correcta"""
    # Test: Quien recibe más paga diferencia
    # Test: Sistema cerrado (total dinero = 0)
    # Test: Comisiones calculadas correctamente

def test_matching_algorithm():
    """Verificar algoritmo matching"""
    # Test: Encuentra ciclos k=3
    # Test: Maneja densidad real (5%)
    # Test: Performance aceptable (< 5s)
```

### **TESTS INTEGRACIÓN:**
- API endpoints
- Flujos completos usuario
- Integración pagos
- Notificaciones

## 📈 ROADMAP

### **FASE 1 (MVP - 1-2 meses):**
- [ ] Backend básico funcionando
- [ ] Algoritmo matching integrado
- [ ] API REST documentada
- [ ] Autenticación usuarios
- [ ] Base de datos PostgreSQL

### **FASE 2 (V1 - 3-4 meses):**
- [ ] Sistema pagos Stripe
- [ ] Notificaciones push/email
- [ ] Dashboard admin
- [ ] App móvil básica
- [ ] Sistema reputación

### **FASE 3 (ESCALABLE - 6+ meses):**
- [ ] Machine learning recomendaciones
- [ ] Chat integrado entre usuarios
- [ ] Sistema envíos/logística
- [ ] Internacionalización
- [ ] Marketplace secundario

## 🎯 CONCLUSIÓN

Esta arquitectura proporciona:
1. **Escalabilidad:** Microservicios + contenedores
2. **Fiabilidad:** Base de datos ACID + transacciones
3. **Seguridad:** Autenticación robusta + encriptación
4. **Mantenibilidad:** Código modular + testing completo
5. **Performance:** Caching + procesamiento asíncrono

**Próximo paso:** Implementar API básica con FastAPI y conectar con algoritmo Treqe corregido.