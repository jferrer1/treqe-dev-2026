#!/bin/bash
# Treqe MVP Quick Start Script
# Run this to set up Treqe MVP development environment

set -e  # Exit on error

echo "🚀 Treqe MVP Quick Start"
echo "========================"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Create project directory
PROJECT_DIR="treqe-mvp"
if [ -d "$PROJECT_DIR" ]; then
    echo "⚠️  Directory $PROJECT_DIR already exists"
    read -p "Do you want to remove it and start fresh? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing directory..."
        rm -rf "$PROJECT_DIR"
    else
        echo "❌ Aborting. Please remove or rename the existing directory."
        exit 1
    fi
fi

echo "📁 Creating project structure..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create monorepo structure
echo "🏗️  Setting up monorepo structure..."
mkdir -p apps/web/app
mkdir -p apps/web/components
mkdir -p apps/web/lib
mkdir -p apps/web/styles
mkdir -p apps/api/src/controllers
mkdir -p apps/api/src/middleware
mkdir -p apps/api/src/models
mkdir -p apps/api/src/routes
mkdir -p apps/api/src/services
mkdir -p packages/database
mkdir -p packages/types
mkdir -p packages/utils

# Create root package.json
echo "📦 Creating root package.json..."
cat > package.json << 'EOF'
{
  "name": "treqe-mvp",
  "version": "0.1.0",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "start": "turbo start",
    "lint": "turbo lint",
    "test": "turbo test",
    "db:push": "cd packages/database && npm run push",
    "db:seed": "cd packages/database && npm run seed",
    "clean": "turbo clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^1.13.3",
    "typescript": "^5.3.3"
  },
  "packageManager": "npm@10.2.4",
  "engines": {
    "node": ">=18.0.0"
  }
}
EOF

# Create turbo.json
echo "⚡ Creating turbo.json..."
cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
EOF

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Next.js
.next/
out/

# Production
build
dist

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs
*.log

# Database
*.db
*.sqlite
EOF

# Create .env.example
echo "🔧 Creating .env.example..."
cat > .env.example << 'EOF'
# Database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/treqe"
DIRECT_URL="postgresql://postgres:postgres@localhost:5432/treqe"

# Redis
REDIS_URL="redis://localhost:6379"

# Authentication
NEXTAUTH_SECRET="your-nextauth-secret-here-change-in-production"
NEXTAUTH_URL="http://localhost:3000"

# Upload
UPLOADTHING_SECRET="sk_live_xxxx"
UPLOADTHING_APP_ID="xxxx"

# Email (optional)
RESEND_API_KEY="re_xxxx"
EMAIL_FROM="noreply@treqe.es"

# Analytics (optional)
SENTRY_DSN="https://xxxx@sentry.io/xxxx"
EOF

# Create README.md
echo "📚 Creating README.md..."
cat > README.md << 'EOF'
# 🚀 Treqe MVP

A modern marketplace for circular exchanges with structured offers and reputation system.

## 🎯 Features

- **Structured Offer System** (Opción A validated)
- **Circular Matching Algorithm** (k=3 optimal)
- **User Reputation System**
- **Real-time Notifications**
- **Secure Authentication**

## 🏗️ Architecture

- **Frontend:** Next.js 15 (App Router) + Tailwind CSS
- **Backend:** Node.js + Express
- **Database:** PostgreSQL + Redis
- **Authentication:** NextAuth.js
- **Deployment:** Vercel + Railway

## 🚀 Quick Start

1. **Clone and install:**
   ```bash
   git clone <repository>
   cd treqe-mvp
   npm install
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your values
   ```

3. **Start database:**
   ```bash
   docker-compose up -d postgres redis
   ```

4. **Set up database schema:**
   ```bash
   npm run db:push
   npm run db:seed
   ```

5. **Start development servers:**
   ```bash
   npm run dev
   ```

6. **Open in browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:3001

## 📁 Project Structure

```
treqe-mvp/
├── apps/
│   ├── web/                 # Next.js frontend
│   └── api/                 # Express backend
├── packages/
│   ├── database/           # Database schema & migrations
│   ├── types/             # Shared TypeScript types
│   └── utils/             # Shared utilities
├── docker-compose.yml      # Local development services
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- --testPathPattern=unit
```

## 🚢 Deployment

### Frontend (Vercel):
```bash
cd apps/web
vercel --prod
```

### Backend (Railway):
```bash
cd apps/api
railway up
```

## 📄 License

MIT
EOF

# Create docker-compose.yml
echo "🐳 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: treqe
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
EOF

echo ""
echo "✅ Treqe MVP starter kit created in ./$PROJECT_DIR/"
echo ""
echo "📋 Next steps:"
echo "1. cd $PROJECT_DIR"
echo "2. npm install"
echo "3. cp .env.example .env.local"
echo "4. Edit .env.local with your values"
echo "5. docker-compose up -d"
echo "6. npm run dev"
echo ""
echo "🌐 Frontend will be at: http://localhost:3000"
echo "🔌 Backend API will be at: http://localhost:3001"
echo ""
echo "🚀 Happy coding!"