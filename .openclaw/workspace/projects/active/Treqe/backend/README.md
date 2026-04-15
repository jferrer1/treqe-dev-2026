# Treqe Backend

Circular exchange matching platform with correct economic logic.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL (included in Docker)

### Using Docker (Recommended)

1. **Clone and setup**
```bash
cd projects/Treqe/backend
cp .env.example .env
# Edit .env if needed
```

2. **Start services**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379
- Treqe API on port 8000
- PgAdmin on port 5050 (optional)
- Redis Commander on port 8081 (optional)

3. **Access the API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Manual Setup (Development)

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Run database migrations**
```bash
# Initialize database (creates tables)
python -c "from src.database.connection import init_db; import asyncio; asyncio.run(init_db())"
```

4. **Run the API**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
src/
├── api/                  # FastAPI endpoints
│   ├── auth.py          # JWT authentication
│   ├── schemas.py       # Pydantic schemas
│   ├── users.py         # User management
│   ├── items.py         # Item management
│   ├── preferences.py   # Preference management
│   ├── matching.py      # Exchange matching
│   └── proposals.py     # Exchange proposals
├── core/                # Business logic
│   ├── matching.py      # Matching engine
│   └── algorithm.py     # Core algorithm (advanced)
├── database/            # Database layer
│   ├── models.py        # SQLAlchemy models
│   └── connection.py    # DB connection
└── utils/              # Utilities
    ├── config.py       # Configuration
    └── logger.py       # Logging
```

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login (get JWT tokens)
- `GET /api/v1/users/me` - Get current user info

### Items
- `POST /api/v1/items` - Create item
- `GET /api/v1/items` - List items (with filters)
- `GET /api/v1/items/{id}` - Get item details
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### Preferences
- `POST /api/v1/preferences` - Create preference
- `GET /api/v1/preferences` - List preferences
- `PUT /api/v1/preferences/{id}` - Update preference
- `DELETE /api/v1/preferences/{id}` - Delete preference

### Matching
- `POST /api/v1/matching/find` - Find exchanges
- `GET /api/v1/matching/status` - Get matching status
- `GET /api/v1/matching/recommendations` - Get improvement recommendations

### Proposals
- `GET /api/v1/proposals` - List proposals
- `GET /api/v1/proposals/{id}` - Get proposal details
- `POST /api/v1/proposals/{id}/accept` - Accept proposal
- `POST /api/v1/proposals/{id}/reject` - Reject proposal

## 💡 Key Features

### 1. Correct Economic Logic
- **Rule**: Whoever receives item of HIGHER value → PAYS the difference
- **Rule**: Whoever gives item of HIGHER value → RECEIVES the difference
- **Closed system**: Total money = 0
- **No magic**: Same economic outcome as sell+buy, but with convenience

### 2. Market Transformation
- Current market (k=2): ~5% probability of exchange
- With Treqe (k=2→6): ~75% probability (15x improvement)
- Creates possibilities where none existed before

### 3. Transparent Proposals
- Clear breakdown of what you give/receive/pay/receive
- Benefits explained in simple terms
- 1-click acceptance
- Everything managed by Treqe

## 🧪 Testing

### Generate Demo Data
```bash
# Use the demo endpoints (development only)
POST /api/v1/proposals/demo/generate?count=3
```

### Test Matching
```bash
# Test different scenarios
POST /api/v1/matching/test-match?scenario=direct
POST /api/v1/matching/test-match?scenario=cycle
POST /api/v1/matching/test-match?scenario=complex
```

### Example Exchange Cycle
```
User A: iPhone €600 → MacBook €800 → PAYS €200 difference
User B: MacBook €800 → Bicycle €400 → RECEIVES €400 difference
User C: Bicycle €400 → iPhone €600 → PAYS €200 difference

Money flow (6% commissions):
A → Treqe: €212 (€200 diff + €12 commission)
Treqe → B: €376 (€400 diff - €24 commission)
C → Treqe: €212 (€200 diff + €12 commission)
```

## 🔒 Security

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- Rate limiting per user/IP
- CORS configured
- Input validation with Pydantic

## 📊 Monitoring

- Health endpoint: `/health`
- Structured logging to file and console
- Database connection pooling
- Request/response logging

## 🚢 Deployment

### Production Considerations
1. Set `ENVIRONMENT=production` in `.env`
2. Use strong `SECRET_KEY`
3. Configure proper `CORS_ORIGINS`
4. Set up database backups
5. Configure monitoring/alerting

### Docker Production
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📈 Next Steps

### Phase 1 (Current - MVP)
- [x] Basic API structure
- [x] User authentication
- [x] Item management
- [x] Preference management
- [x] Matching engine
- [x] Proposal system
- [ ] Payment integration
- [ ] Email notifications

### Phase 2
- [ ] Real-time matching
- [ ] Advanced algorithm optimization
- [ ] User reputation system
- [ ] Dispute resolution
- [ ] Mobile app

### Phase 3
- [ ] Machine learning recommendations
- [ ] International expansion
- [ ] Logistics integration
- [ ] Marketplace features

## 🐛 Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check PostgreSQL is running
   - Verify credentials in `.env`
   - Check port 5432 is available

2. **API not starting**
   - Check Python version (3.11+)
   - Verify all dependencies installed
   - Check port 8000 is available

3. **CORS errors**
   - Update `CORS_ORIGINS` in `.env`
   - Ensure frontend URL is included

### Logs
```bash
# Docker logs
docker-compose logs api
docker-compose logs postgres

# Application logs
tail -f logs/treqe.log
```

## 📚 Documentation

- API Documentation: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json
- Source: https://github.com/your-repo/treqe

## 🆘 Support

- Check the docs first
- Look at existing issues
- Create detailed bug reports
- Include logs and reproduction steps

## 📄 License

Proprietary - All rights reserved.

---

**Treqe doesn't create magical value - it creates possibilities where none existed before.**