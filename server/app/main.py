from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.config import settings

#Create fast api
app= FastAPI(
    title="GMGN Trading API",
    description= "FastAPI backend Crypto trading platform",
    version= "1.0.0",
    docs_url="/docs", #swagger UI at /docs
    redoc_url="/redoc" # ReDoc at /redoc
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#Include routes
app.include_router(auth.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"status": "OK", "message": "GMGN API is running"}

@app.get("/")
def root():
    return {"message": "GMGN Trading API", "docs": "/docs"}

