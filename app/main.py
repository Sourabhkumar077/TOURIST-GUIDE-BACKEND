from datetime import datetime
from fastapi import FastAPI
from .database import Base, engine
from .routes import auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Tourist Safety System")

# Include Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])


@app.get("/")
def test():
    return {"message": "wellcome"}


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}