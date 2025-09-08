# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import your existing routes if they exist
try:
    from app.routes import auth
    ROUTES_EXIST = True
except ImportError:
    ROUTES_EXIST = False
    print("Routes not found, using basic setup")

# Import database setup
try:
    from app.database.connection import init_db, close_db
    DATABASE_SETUP = True
except ImportError:
    DATABASE_SETUP = False
    print("Database setup not found, skipping DB initialization")

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting GMGN Trading API...")
    
    if DATABASE_SETUP:
        await init_db()
        print("✅ Database initialized!")
    else:
        print("Database not configured")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down GMGN Trading API...")
    if DATABASE_SETUP:
        await close_db()
    print("👋 Goodbye!")

# Create FastAPI app
app = FastAPI(
    title="GMGN Trading API",
    description="FastAPI backend for Crypto Trading Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan if DATABASE_SETUP else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes if they exist
if ROUTES_EXIST:
    app.include_router(auth.router, prefix="/api")

# Basic routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "GMGN API v2.0 is running!",
        "database": "PostgreSQL" if DATABASE_SETUP else "Not configured",
        "routes": "Loaded" if ROUTES_EXIST else "Basic"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GMGN Trading API v2.0",
        "docs": "/docs",
        "health": "/api/health"
    }

# Test endpoint
@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify server is working"""
    return {
        "success": True,
        "message": "Server is working!",
        "database_configured": DATABASE_SETUP,
        "routes_configured": ROUTES_EXIST
    }