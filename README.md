🛰️ Smart Tourist Safety Monitoring & Incident Response System - Backend

A FastAPI-based backend for monitoring tourist safety, managing incident reports, and enabling real-time emergency response using AI, Blockchain (planned), and Geo-Fencing (planned) integrations.

🚀 Features

Authentication

JWT-based authentication (login, token validation)

Role-based access (Tourist / Responder / Admin)

Tourist Management

Register tourists with UUID Digital Tourist ID

Profile fetch, update, delete

Emergency contacts & itinerary storage

Incident Management

Report incidents (linked to tourists)

Fetch tourist-specific incidents

Update incident status (open → resolved)

System

Health check & root endpoints

Logging middleware with timing

Global error handling with JSON responses

🏗️ Tech Stack

Backend: FastAPI

Database: PostgreSQL (default) / SQLite (dev mode)

ORM: SQLAlchemy + Pydantic

Auth: JWT (PyJWT, OAuth2PasswordBearer)

Migrations: Alembic (recommended)

Logging: Built-in logging module

Deployment Ready: .env config support, CORS enabled

📂 Project Structure
backend/
├── app/
│   ├── main.py              # App initialization
│   ├── config.py            # Environment settings
│   ├── database.py          # DB connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── routes/
│   │   ├── auth.py          # JWT Auth endpoints
│   │   ├── tourist.py       # Tourist endpoints
│   │   ├── incident.py      # Incident endpoints
│   ├── __init__.py
│
├── requirements.txt         # Dependencies
├── .env                     # Env variables template
└── README.md

⚙️ Setup & Installation
1️⃣ Clone Repository
git clone https://github.com/your-org/tourist-safety-backend.git
cd tourist-safety-backend/backend

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment

Create .env file (copy .env.example if exists):

DATABASE_URL=postgresql://user:password@localhost:5432/tourist_safety
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000

5️⃣ Run Application
uvicorn app.main:app --reload


Visit Swagger Docs: 👉 http://127.0.0.1:8000/docs

🔑 API Endpoints (Summary)
Auth

POST /auth/login → Login & get JWT

GET /auth/me → Get current user

Tourists

POST /tourist/register → Register new tourist

GET /tourist/{id} → Get tourist profile

PUT /tourist/{id} → Update tourist

DELETE /tourist/{id} → Delete tourist

GET /tourist/ → List tourists (pagination)

Incidents

POST /incident/report → Report incident

GET /incident/{tourist_id} → Get incidents for tourist

PUT /incident/{incident_id}/status → Update incident status

System

GET /health → Health check

GET / → API root info

🧪 Running Tests

Tests use pytest:

pytest

🛠️ Deployment Notes

Use PostgreSQL in production, SQLite is only for dev/demo.

Add Alembic migrations for schema changes:

alembic init migrations


Configure Gunicorn/Uvicorn workers for scaling.

Add reverse proxy (Nginx/Traefik) for deployment.

📌 Roadmap

 AI-based anomaly detection (location drop, inactivity)

 Blockchain for tamper-proof tourist IDs

 Geo-fencing alerts integration

 IoT wearable device integration

 Multilingual support in APIs