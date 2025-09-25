import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Sourabh2025Secure@localhost:5432/saarthi_db")

# API Configuration
API_V1_STR = "/api"
PROJECT_NAME = "Saarthi"

# CORS Configuration
BACKEND_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:19006",
    "http://127.0.0.1:19006",
    "http://127.0.0.1:3000",
    "http://192.168.43.158:19006",  # Your phone's Expo connection
    "http://192.168.43.158:3000",   # Alternative port
    "exp://192.168.43.158:19000"    # Expo tunnel URL
]
