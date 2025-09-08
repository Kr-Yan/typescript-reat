# main.py (Updated for Raw SQL)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# from app.routes import auth
from app.config import settings
from app.database.connection import init_db, close_db
from app.routes import auth


# Lifespan event handler for database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting GMGN Trading API with Raw SQL...")
    await init_db()
    print("✅ Database initialized with Raw SQL!")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down GMGN Trading API...")
    await close_db()
    print("👋 Goodbye!")

# Create FastAPI app with lifespan
app = FastAPI(
    title="GMGN Trading API",
    description="FastAPI backend with Raw SQL and PostgreSQL",
    version="2.0.0-raw-sql",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(auth.router, prefix="/api")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "GMGN API v2.0 with Raw SQL is running!",
        "database": "PostgreSQL with Raw SQL",
        "version": "2.0.0-raw-sql"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GMGN Trading API v2.0 - Raw SQL Edition",
        "docs": "/docs",
        "health": "/api/health",
        "database": "Raw SQL + asyncpg"
    }

# Debug endpoint to test raw SQL
@app.get("/api/debug/users")
async def debug_users():
    """Debug endpoint to see raw SQL in action"""
    from app.database.connection import execute_query
    
    query = """
        SELECT 
            id, 
            email, 
            name, 
            balance, 
            created_at,
            CASE 
                WHEN balance > 50 THEN 'High Balance'
                WHEN balance > 10 THEN 'Medium Balance'
                ELSE 'Low Balance'
            END as balance_category
        FROM users 
        WHERE is_active = TRUE
        ORDER BY created_at DESC
        LIMIT 10
    """
    
    results = await execute_query(query)
    return [dict(row) for row in results]