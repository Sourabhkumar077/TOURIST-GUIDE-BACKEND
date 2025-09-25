from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth, tourist, authority
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BACKEND_CORS_ORIGINS

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Tourist Safety System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tourist.router, prefix="/api/tourist", tags=["Tourist"])
app.include_router(authority.router, prefix="/api/authority", tags=["Authority"])


@app.get("/")
def test():
    return {"message": "Welcome to Saarthi - Smart Tourist Safety System"}


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}